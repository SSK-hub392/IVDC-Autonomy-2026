import argparse
from collections import deque
from heapq import heappop, heappush
from itertools import count
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


def build_default_grid():
    grid = np.zeros((18, 26), dtype=np.uint8)
    grid[5:8, 3:20] = 1
    grid[10:12, 7:24] = 1
    grid[5:8, 12] = 0
    grid[10:12, 18] = 0
    return grid


def check_position(grid, position, name):
    if not isinstance(position, (tuple, list)) or len(position) != 2:
        raise ValueError(f"{name} must be a row and column pair")
    row, column = position
    if not isinstance(row, (int, np.integer)) or not isinstance(column, (int, np.integer)):
        raise ValueError(f"{name} row and column must be whole numbers")
    if not (0 <= row < grid.shape[0] and 0 <= column < grid.shape[1]):
        raise ValueError(f"{name} is outside the grid")
    if grid[row, column] != 0:
        raise ValueError(f"{name} must be on a free cell")
    return int(row), int(column)


def get_neighbours(grid, position):
    row, column = position
    options = ((row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1))
    return [
        (next_row, next_column)
        for next_row, next_column in options
        if 0 <= next_row < grid.shape[0]
        and 0 <= next_column < grid.shape[1]
        and grid[next_row, next_column] == 0
    ]


def make_result(parent, explored, goal, cost):
    if goal not in parent:
        return {"found": False, "path": [], "explored": explored,
                "path_length": None, "path_cost": None}
    path = []
    position = goal
    while position is not None:
        path.append(position)
        position = parent[position]
    path.reverse()
    return {
        "found": True,
        "path": path,
        "explored": explored,
        "path_length": len(path) - 1,
        "path_cost": cost,
    }


def breadth_first_search(grid, start, goal):
    grid = np.asarray(grid)
    if grid.ndim != 2:
        raise ValueError("The map must be a 2D grid")
    start = check_position(grid, start, "Start")
    goal = check_position(grid, goal, "Goal")
    frontier = deque([start])
    parent = {start: None}
    explored = []
    while frontier:
        current = frontier.popleft()
        explored.append(current)
        if current == goal:
            break
        for neighbour in get_neighbours(grid, current):
            if neighbour not in parent:
                parent[neighbour] = current
                frontier.append(neighbour)
    result = make_result(parent, explored, goal, None)
    if result["found"]:
        result["path_cost"] = result["path_length"]
    return result


def manhattan_distance(position, goal):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def a_star_search(grid, start, goal):
    grid = np.asarray(grid)
    if grid.ndim != 2:
        raise ValueError("The map must be a 2D grid")
    start = check_position(grid, start, "Start")
    goal = check_position(grid, goal, "Goal")
    tie_breaker = count()
    frontier = [(manhattan_distance(start, goal), next(tie_breaker), 0, start)]
    parent = {start: None}
    cost_so_far = {start: 0}
    explored = []
    while frontier:
        _, _, queued_cost, current = heappop(frontier)
        if queued_cost != cost_so_far[current]:
            continue
        explored.append(current)
        if current == goal:
            break
        for neighbour in get_neighbours(grid, current):
            new_cost = queued_cost + 1
            if new_cost < cost_so_far.get(neighbour, float("inf")):
                cost_so_far[neighbour] = new_cost
                parent[neighbour] = current
                priority = new_cost + manhattan_distance(neighbour, goal)
                heappush(frontier, (priority, next(tie_breaker), new_cost, neighbour))
    return make_result(parent, explored, goal, cost_so_far.get(goal))


def draw_search(grid, start, goal, result, title, output_path):
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.imshow(grid, cmap=plt.matplotlib.colors.ListedColormap(["#f4f7f9", "#263746"]), vmin=0, vmax=1)
    explored = [cell for cell in result["explored"] if cell not in (start, goal)]
    if explored:
        axis.scatter([cell[1] for cell in explored], [cell[0] for cell in explored],
                     marker="s", s=75, color="#9bd3e8", edgecolors="none")
    if result["found"]:
        axis.plot([cell[1] for cell in result["path"]], [cell[0] for cell in result["path"]],
                  color="#df543f", linewidth=3)
    axis.scatter(start[1], start[0], marker="o", s=110, color="#2a9d65")
    axis.scatter(goal[1], goal[0], marker="*", s=180, color="#7455a6")
    axis.set_title(title)
    axis.set_xticks(range(grid.shape[1]))
    axis.set_yticks(range(grid.shape[0]))
    axis.grid(color="white", linewidth=0.45, alpha=0.8)
    axis.set_xlabel("Column")
    axis.set_ylabel("Row")
    axis.legend(handles=[
        Patch(facecolor="#f4f7f9", edgecolor="#808a91", label="Free cell"),
        Patch(facecolor="#263746", label="Obstacle"),
        Patch(facecolor="#9bd3e8", label="Explored cell"),
        Line2D([0], [0], color="#df543f", linewidth=3, label="Chosen path"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#2a9d65", markersize=9, label="Start"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor="#7455a6", markersize=12, label="Goal"),
    ], loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)
    figure.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return output_path


def save_comparison(bfs_result, astar_result, output_path):
    names = ["BFS", "A*"]
    explored_counts = [len(bfs_result["explored"]), len(astar_result["explored"])]
    path_lengths = [bfs_result["path_length"], astar_result["path_length"]]
    figure, axes = plt.subplots(1, 2, figsize=(8, 4))
    axes[0].bar(names, explored_counts, color=["#62b6d0", "#7455a6"])
    axes[0].set_title("Cells explored")
    axes[0].set_ylabel("Number of cells")
    axes[1].bar(names, path_lengths, color=["#62b6d0", "#7455a6"])
    axes[1].set_title("Path length")
    axes[1].set_ylabel("Number of moves")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=160)
    plt.close(figure)
    return output_path


def run_demo(output_folder):
    grid = build_default_grid()
    start = (1, 1)
    goal = (16, 24)
    bfs_result = breadth_first_search(grid, start, goal)
    astar_result = a_star_search(grid, start, goal)
    output_folder = Path(output_folder)
    bfs_image = draw_search(grid, start, goal, bfs_result, "BFS on the example grid", output_folder / "bfs_visualization.png")
    astar_image = draw_search(grid, start, goal, astar_result, "A* on the example grid", output_folder / "astar_visualization.png")
    comparison_image = save_comparison(bfs_result, astar_result, output_folder / "algorithm_comparison.png")
    for name, result in (("BFS", bfs_result), ("A*", astar_result)):
        print(f"{name}: path found = {result['found']}")
        print(f"{name}: explored cells = {len(result['explored'])}")
        print(f"{name}: path length = {result['path_length']}")
        print(f"{name}: path cost = {result['path_cost']}")
    print(f"Start: {start}; goal: {goal}")
    print(f"Saved: {bfs_image.resolve()}")
    print(f"Saved: {astar_image.resolve()}")
    print(f"Saved: {comparison_image.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="Compare BFS and A* on a grid.")
    parser.add_argument("--output-folder", type=Path, default=Path(__file__).parent / "outputs")
    args = parser.parse_args()
    run_demo(args.output_folder)


if __name__ == "__main__":
    main()
