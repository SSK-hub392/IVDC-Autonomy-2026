# PS3 - Controllers and Reinforcement Learning

## Feedback control

A controller compares the wanted value with a measurement. Their difference is the error. A P controller sends a command based on current error: `u = Kp * e`. PID adds the total past error and the rate at which error changes. The local program includes a simple Q-learning grid rather than a vehicle PID simulation; the research PDF explains P and PID.

## Local Frozen-Lake-style grid

The map has 16 states. The agent starts at the top left. `F` is a safe tile, `H` is a terminal hole, and `G` is the goal. It can move up, right, down, or left. Safe moves have a small cost, a hole gives a penalty, and reaching the goal gives a reward.

The Q-table has one row per state and one column per action. `Q(s, a)` estimates future reward for action `a` in state `s`. The update is:

`Q(s, a) = Q(s, a) + alpha * [reward + gamma * max(Q(next_state, next_action)) - Q(s, a)]`

`alpha` controls how much a new result changes the stored value. `gamma` controls how much later rewards count. The future value is zero after reaching a terminal state. Epsilon-greedy selection sometimes tries a random action (exploration) and otherwise uses an action with a high Q value (exploitation).

## Run and change settings

From the project root:

```powershell
.venv\Scripts\python.exe PS3_Controllers_RL\q_learning_frozen_lake.py --episodes 5000 --seed 7 --eval-episodes 100
```

Episode count, seed, step limit, learning rate, discount factor, and exploration settings can be changed with command-line options. Use `--help` to see them. The program prints the learned Q-table, recent training success, and a separate greedy evaluation success rate.

## Outputs and interpretation

The `outputs` folder receives `q_table.csv`, `training_rewards.png`, and `learned_policy.png`. The policy picture shows the map before training beside the learned arrows and route. The evaluation repeatedly tests the greedy policy on the same deterministic map. That success rate only describes this small example; it is not a guarantee on other maps.

## Deep-ML task is separate

The local program is a learning example. It does not complete the assigned website project and cannot pass its platform tests. Follow `../docs/deepml_guide.md` to open the project, work through the listed steps, run the site's own checks, and save the completion screenshot yourself.

## Limitations

The example has one small, deterministic map and a table of values. It does not model slippery movement, changing maps, sensors, or vehicle control. Training results depend on the settings and random seed. A high exploration rate can lead to more hole visits while learning; a low rate can make it harder to discover a useful route.
