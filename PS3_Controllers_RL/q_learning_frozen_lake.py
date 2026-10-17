import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


class FrozenLake:
    def __init__(self):
        self.tiles = ["SFFF", "FHFH", "FFFH", "HFFG"]
        self.rows = len(self.tiles)
        self.columns = len(self.tiles[0])
        self.start_state = 0
        self.goal_state = self.rows * self.columns - 1
        self.hole_states = {5, 7, 11, 12}
        self.action_names = ["up", "right", "down", "left"]
        self.action_moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def state_position(self, state):
        if not isinstance(state, (int, np.integer)) or not 0 <= state < self.rows * self.columns:
            raise ValueError("State is outside the lake")
        return divmod(int(state), self.columns)

    def step(self, state, action):
        row, column = self.state_position(state)
        if not isinstance(action, (int, np.integer)) or not 0 <= action < len(self.action_moves):
            raise ValueError("Action must be 0, 1, 2, or 3")
        change_row, change_column = self.action_moves[int(action)]
        next_row = min(self.rows - 1, max(0, row + change_row))
        next_column = min(self.columns - 1, max(0, column + change_column))
        next_state = next_row * self.columns + next_column
        if next_state in self.hole_states:
            return next_state, -1.0, True
        if next_state == self.goal_state:
            return next_state, 1.0, True
        return next_state, -0.02, False


def validate_parameters(episodes, max_steps, eval_episodes, learning_rate,
                        discount_factor, exploration_rate, min_exploration_rate,
                        exploration_decay):
    if episodes < 1 or max_steps < 1 or eval_episodes < 1:
        raise ValueError("Episode counts and maximum steps must be positive")
    if not 0 < learning_rate <= 1:
        raise ValueError("Learning rate must be greater than 0 and at most 1")
    if not 0 <= discount_factor <= 1:
        raise ValueError("Discount factor must be between 0 and 1")
    if not 0 <= min_exploration_rate <= exploration_rate <= 1:
        raise ValueError("Exploration rates must satisfy 0 <= minimum <= initial <= 1")
    if not 0 < exploration_decay <= 1:
        raise ValueError("Exploration decay must be greater than 0 and at most 1")


def choose_action(q_table, state, exploration_rate, random_generator):
    if random_generator.random() < exploration_rate:
        return int(random_generator.integers(q_table.shape[1]))
    best_value = np.max(q_table[state])
    best_actions = np.flatnonzero(np.isclose(q_table[state], best_value))
    return int(random_generator.choice(best_actions))


def update_q_value(q_table, state, action, reward, next_state, terminal,
                   learning_rate, discount_factor):
    future_value = 0.0 if terminal else discount_factor * np.max(q_table[next_state])
    target = reward + future_value
    error = target - q_table[state, action]
    q_table[state, action] += learning_rate * error


def train_agent(environment, episodes=5000, max_steps=60, seed=7,
                learning_rate=0.18, discount_factor=0.95,
                exploration_rate=1.0, min_exploration_rate=0.03,
                exploration_decay=0.998):
    validate_parameters(episodes, max_steps, 1, learning_rate,
                        discount_factor, exploration_rate,
                        min_exploration_rate, exploration_decay)
    random_generator = np.random.default_rng(seed)
    q_table = np.zeros((environment.rows * environment.columns,
                        len(environment.action_moves)), dtype=float)
    episode_rewards = []
    episode_successes = []
    current_exploration = exploration_rate
    for _ in range(episodes):
        state = environment.start_state
        total_reward = 0.0
        reached_goal = False
        for _ in range(max_steps):
            action = choose_action(q_table, state, current_exploration, random_generator)
            next_state, reward, terminal = environment.step(state, action)
            update_q_value(q_table, state, action, reward, next_state, terminal,
                           learning_rate, discount_factor)
            total_reward += reward
            state = next_state
            if terminal:
                reached_goal = state == environment.goal_state
                break
        episode_rewards.append(total_reward)
        episode_successes.append(reached_goal)
        current_exploration = max(min_exploration_rate,
                                  current_exploration * exploration_decay)
    return q_table, np.asarray(episode_rewards), np.asarray(episode_successes, dtype=bool)


def follow_greedy_policy(environment, q_table, max_steps=60):
    state = environment.start_state
    route = [state]
    reached_goal = False
    for _ in range(max_steps):
        action = int(np.argmax(q_table[state]))
        state, _, terminal = environment.step(state, action)
        route.append(state)
        if terminal:
            reached_goal = state == environment.goal_state
            break
    return {"reached_goal": reached_goal, "route": route}


def evaluate_policy(environment, q_table, episodes=100, max_steps=60):
    if episodes < 1 or max_steps < 1:
        raise ValueError("Evaluation episode counts and maximum steps must be positive")
    successes = 0
    first_route = []
    for episode in range(episodes):
        result = follow_greedy_policy(environment, q_table, max_steps)
        successes += int(result["reached_goal"])
        if episode == 0:
            first_route = result["route"]
    return {"successes": successes, "episodes": episodes,
            "success_rate": successes / episodes, "route": first_route}


def draw_environment_and_policy(environment, q_table, route, output_path):
    figure, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    for axis in axes:
        axis.set_xlim(-0.5, environment.columns - 0.5)
        axis.set_ylim(environment.rows - 0.5, -0.5)
        axis.set_xticks(range(environment.columns))
        axis.set_yticks(range(environment.rows))
        axis.grid(color="#c3cbd1", linewidth=0.8)
        axis.set_aspect("equal")
    for row in range(environment.rows):
        for column in range(environment.columns):
            state = row * environment.columns + column
            tile = environment.tiles[row][column]
            colour = "#8acb88" if tile == "F" else "#263746" if tile == "H" else "#ffffff"
            for axis in axes:
                axis.add_patch(plt.Rectangle((column - 0.5, row - 0.5), 1, 1,
                                             facecolor=colour, edgecolor="#c3cbd1"))
            if tile == "S":
                for axis in axes:
                    axis.text(column, row, "S", ha="center", va="center", weight="bold")
            elif tile == "G":
                for axis in axes:
                    axis.text(column, row, "G", ha="center", va="center", weight="bold")
            elif tile == "H":
                for axis in axes:
                    axis.text(column, row, "H", ha="center", va="center", color="white", weight="bold")
            if tile not in ("S", "G", "H"):
                action = int(np.argmax(q_table[state]))
                axes[1].text(column, row, ["^", ">", "v", "<"][action],
                             ha="center", va="center", fontsize=15, color="#22313f")
    if route:
        route_rows, route_columns = zip(*(environment.state_position(state) for state in route))
        axes[1].plot(route_columns, route_rows, color="#e6533c", linewidth=2.5, marker="o", markersize=4)
    axes[0].set_title("Map before training")
    axes[1].set_title("Greedy policy after training")
    axes[0].set_ylabel("Row")
    for axis in axes:
        axis.set_xlabel("Column")
    map_legend = [
        Patch(facecolor="#8acb88", edgecolor="#c3cbd1", label="Safe tile"),
        Patch(facecolor="#263746", label="Hole"),
    ]
    axes[0].legend(handles=map_legend, loc="upper center",
                   bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)
    axes[1].legend(handles=map_legend + [
        Line2D([0], [0], color="#e6533c", marker="o", label="Greedy route"),
    ], loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False)
    figure.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return output_path


def draw_rewards(episode_rewards, output_path):
    window = min(100, len(episode_rewards))
    average_rewards = np.convolve(episode_rewards, np.ones(window) / window, mode="valid")
    figure, axis = plt.subplots(figsize=(7, 4))
    axis.plot(np.arange(window - 1, len(episode_rewards)), average_rewards, color="#176b87")
    axis.set_title(f"Average reward over the last {window} episodes")
    axis.set_xlabel("Episode")
    axis.set_ylabel("Average reward")
    axis.grid(alpha=0.25)
    figure.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=160)
    plt.close(figure)
    return output_path


def save_q_table(environment, q_table, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(output_path, q_table, delimiter=",", fmt="%.4f",
               header=",".join(environment.action_names), comments="")
    return output_path


def print_q_table(environment, q_table):
    print("Q-table columns: " + ", ".join(environment.action_names))
    for state, values in enumerate(q_table):
        row, column = environment.state_position(state)
        print(f"state ({row}, {column}): " + ", ".join(f"{value:.3f}" for value in values))


def run_experiment(episodes, seed, max_steps, eval_episodes, output_folder,
                   learning_rate, discount_factor, exploration_rate,
                   min_exploration_rate, exploration_decay):
    environment = FrozenLake()
    q_table, episode_rewards, episode_successes = train_agent(
        environment, episodes, max_steps, seed, learning_rate,
        discount_factor, exploration_rate, min_exploration_rate,
        exploration_decay,
    )
    evaluation = evaluate_policy(environment, q_table, eval_episodes, max_steps)
    output_folder = Path(output_folder)
    table_path = save_q_table(environment, q_table, output_folder / "q_table.csv")
    policy_path = draw_environment_and_policy(
        environment, q_table, evaluation["route"], output_folder / "learned_policy.png"
    )
    reward_path = draw_rewards(episode_rewards, output_folder / "training_rewards.png")
    recent_count = min(100, episodes)
    recent_success_rate = float(np.mean(episode_successes[-recent_count:]))
    print(f"Training episodes: {episodes}")
    print(f"Seed: {seed}")
    print(f"Training success rate in the last {recent_count} episodes: {recent_success_rate:.1%}")
    print(f"Greedy evaluation: {evaluation['successes']} / {evaluation['episodes']} goals reached")
    print(f"Greedy evaluation success rate: {evaluation['success_rate']:.1%}")
    print_q_table(environment, q_table)
    print(f"Saved: {table_path.resolve()}")
    print(f"Saved: {policy_path.resolve()}")
    print(f"Saved: {reward_path.resolve()}")
    return {"environment": environment, "q_table": q_table,
            "episode_rewards": episode_rewards, "episode_successes": episode_successes,
            "evaluation": evaluation}


def main():
    parser = argparse.ArgumentParser(description="Train a tabular Q-learning FrozenLake agent.")
    parser.add_argument("--episodes", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--max-steps", type=int, default=60)
    parser.add_argument("--eval-episodes", type=int, default=100)
    parser.add_argument("--learning-rate", type=float, default=0.18)
    parser.add_argument("--discount-factor", type=float, default=0.95)
    parser.add_argument("--exploration-rate", type=float, default=1.0)
    parser.add_argument("--min-exploration-rate", type=float, default=0.03)
    parser.add_argument("--exploration-decay", type=float, default=0.998)
    parser.add_argument("--output-folder", type=Path, default=Path(__file__).parent / "outputs")
    args = parser.parse_args()
    validate_parameters(args.episodes, args.max_steps, args.eval_episodes,
                        args.learning_rate, args.discount_factor,
                        args.exploration_rate, args.min_exploration_rate,
                        args.exploration_decay)
    run_experiment(args.episodes, args.seed, args.max_steps, args.eval_episodes,
                   args.output_folder, args.learning_rate, args.discount_factor,
                   args.exploration_rate, args.min_exploration_rate,
                   args.exploration_decay)


if __name__ == "__main__":
    main()
