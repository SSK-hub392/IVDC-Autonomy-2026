"""Compare two ways to find a route through a simple grid map.

Breadth-first search (BFS) checks nearby cells in order. A* uses the same map,
but gives priority to cells that seem closer to the goal. Both allow only
up, down, left, and right moves, and assume every move has the same cost.
"""

import argparse
from collections import deque
from heapq import heappop, heappush
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


def build_default_grid():
    """Create the example map: 0 is open space and 1 is an obstacle."""
    rows = 18
    columns = 26
    grid = np.zeros((rows, columns), dtype=np.uint8)

    # Add two horizontal obstacle blocks. Grid slices do not include the end.
    grid[5:8, 3:20] = 1
    grid[10:12, 7:24] = 1

    # Leave two openings in the obstacle blocks so a route can pass through.
    grid[5:8, 12] = 0
    grid[10:12, 18] = 0
    return grid


def check_position(grid, position, name):
    """Check that a start or goal is a valid (row, column) open cell."""
    if not isinstance(position, (tuple, list)) or len(position) != 2:
        raise ValueError(f"{name} must be a row and column pair")

    row, column = position
    if not isinstance(row, (int, np.integer)) or not isinstance(column, (int, np.integer)):
        raise ValueError(f"{name} row and column must be whole numbers")

    if not (0 <= row < grid.shape[0] and 0 <= column < grid.shape[1]):
        raise ValueError(f"{name} is outside the grid")

    if grid[row, column] != 0:
        raise ValueError(f"{name} must be on a free cell")

    # Return normal Python integers so positions can be used as dictionary keys.
    return int(row), int(column)


def get_neighbours(grid, position):
    """Return the open cells directly above, below, left, and right."""
    row, column = position

    possible_moves = [
        (row - 1, column),  # up
        (row + 1, column),  # down
        (row, column - 1),  # left
        (row, column + 1),  # right
    ]

    neighbours = []
    for next_row, next_column in possible_moves:
        inside_grid = (
            0 <= next_row < grid.shape[0]
            and 0 <= next_column < grid.shape[1]
        )
        if inside_grid and grid[next_row, next_column] == 0:
            neighbours.append((next_row, next_column))

    return neighbours


def make_result(parent, explored, goal, cost):
    """Build a result dictionary and follow parent links to recover the path."""
    if goal not in parent:
        return {
            "found": False,
            "path": [],
            "explored": explored,
            "path_length": None,
            "path_cost": None,
        }

    # Each cell remembers which cell we came from. Follow those links backward.
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]

    # The links led from goal back to start, so reverse the list for display.
    path.reverse()

    return {
        "found": True,
        "path": path,
        "explored": explored,
        "path_length": len(path) - 1,
        "path_cost": cost,
    }


def breadth_first_search(grid, start, goal):
    """Find a shortest route when all moves have equal cost."""
    grid = np.asarray(grid)
    if grid.ndim != 2:
        raise ValueError("The map must be a 2D grid")

    start = check_position(grid, start, "Start")
    goal = check_position(grid, goal, "Goal")

    # deque is a queue: the first cell added is the first one removed.
    cells_to_visit = deque([start])

    # 'parent' also acts as our visited set. Start has no previous cell.
    parent = {start: None}
    explored = []

    while cells_to_visit:
        current = cells_to_visit.popleft()
        explored.append(current)

        if current == goal:
            break

        for neighbour in get_neighbours(grid, current):
            # Only add a cell once. This prevents looping back and forth.
            if neighbour not in parent:
                parent[neighbour] = current
                cells_to_visit.append(neighbour)

    result = make_result(parent, explored, goal, None)

    # In this map every move costs one, so cost equals the number of moves.
    if result["found"]:
        result["path_cost"] = result["path_length"]

    return result


def manhattan_distance(position, goal):
    """Count row and column steps to the goal, ignoring obstacles."""
    row_steps = abs(position[0] - goal[0])
    column_steps = abs(position[1] - goal[1])
    return row_steps + column_steps


def a_star_search(grid, start, goal):
    """Find a shortest route while using distance-to-goal to guide the search."""
    grid = np.asarray(grid)
    if grid.ndim != 2:
        raise ValueError("The map must be a 2D grid")

    start = check_position(grid, start, "Start")
    goal = check_position(grid, goal, "Goal")

    # The priority queue always removes the entry with the smallest priority.
    # Each entry stores: (estimated_total_cost, cost_so_far, grid_position).
    first_estimate = manhattan_distance(start, goal)
    priority_queue = [(first_estimate, 0, start)]

    parent = {start: None}
    cost_so_far = {start: 0}
    explored = []

    while priority_queue:
        estimated_total, queued_cost, current = heappop(priority_queue)

        # A cell may get a better route after an older entry was queued.
        # Ignore that old entry if its cost no longer matches the best cost.
        if queued_cost != cost_so_far[current]:
            continue

        explored.append(current)
        if current == goal:
            break

        for neighbour in get_neighbours(grid, current):
            new_cost = queued_cost + 1

            # Keep this route only if it is cheaper than any route found before.
            if new_cost < cost_so_far.get(neighbour, float("inf")):
                cost_so_far[neighbour] = new_cost
                parent[neighbour] = current

                # A* priority = moves already taken + estimated moves remaining.
                estimate_to_goal = manhattan_distance(neighbour, goal)
                priority = new_cost + estimate_to_goal
                heappush(priority_queue, (priority, new_cost, neighbour))

    return make_result(parent, explored, goal, cost_so_far.get(goal))


def draw_search(grid, start, goal, result, title, output_path):
    """Draw the map, the cells explored, and the route chosen by one search."""
    figure, axis = plt.subplots(figsize=(10, 6))

    # Show free cells as light squares and obstacles as dark squares.
    map_colours = plt.matplotlib.colors.ListedColormap(["#f4f7f9", "#263746"])
    axis.imshow(grid, cmap=map_colours, vmin=0, vmax=1)

    # Draw explored cells, but don't cover the start or goal markers.
    explored_without_endpoints = [
        cell for cell in result["explored"] if cell not in (start, goal)
    ]
    if explored_without_endpoints:
        axis.scatter(
            [cell[1] for cell in explored_without_endpoints],
            [cell[0] for cell in explored_without_endpoints],
            marker="s",
            s=75,
            color="#9bd3e8",
            edgecolors="none",
        )

    # A path is a list of (row, column) cells. Plots need x=column, y=row.
    if result["found"]:
        axis.plot(
            [cell[1] for cell in result["path"]],
            [cell[0] for cell in result["path"]],
            color="#df543f",
            linewidth=3,
        )

    axis.scatter(start[1], start[0], marker="o", s=110, color="#2a9d65")
    axis.scatter(goal[1], goal[0], marker="*", s=180, color="#7455a6")

    axis.set_title(title)
    axis.set_xticks(range(grid.shape[1]))
    axis.set_yticks(range(grid.shape[0]))
    axis.grid(color="white", linewidth=0.45, alpha=0.8)
    axis.set_xlabel("Column")
    axis.set_ylabel("Row")

    # Build a legend so the colours and symbols are easy to understand.
    legend_items = [
        Patch(facecolor="#f4f7f9", edgecolor="#808a91", label="Free cell"),
        Patch(facecolor="#263746", label="Obstacle"),
        Patch(facecolor="#9bd3e8", label="Explored cell"),
        Line2D([0], [0], color="#df543f", linewidth=3, label="Chosen path"),
        Line2D(
            [0], [0], marker="o", color="w", markerfacecolor="#2a9d65",
            markersize=9, label="Start",
        ),
        Line2D(
            [0], [0], marker="*", color="w", markerfacecolor="#7455a6",
            markersize=12, label="Goal",
        ),
    ]
    axis.legend(
        handles=legend_items,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False,
    )

    figure.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return output_path


def save_comparison(bfs_result, astar_result, output_path):
    """Save a bar chart comparing how many cells BFS and A* explored."""
    search_names = ["BFS", "A*"]
    explored_counts = [
        len(bfs_result["explored"]),
        len(astar_result["explored"]),
    ]
    path_lengths = [
        bfs_result["path_length"],
        astar_result["path_length"],
    ]

    figure, axes = plt.subplots(1, 2, figsize=(8, 4))

    axes[0].bar(search_names, explored_counts, color=["#62b6d0", "#7455a6"])
    axes[0].set_title("Cells explored")
    axes[0].set_ylabel("Number of cells")

    axes[1].bar(search_names, path_lengths, color=["#62b6d0", "#7455a6"])
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
    """Run both searches on the example map and save their pictures."""
    grid = build_default_grid()
    start = (1, 1)  # (row, column), near the upper-left corner
    goal = (16, 24)  # (row, column), near the lower-right corner

    bfs_result = breadth_first_search(grid, start, goal)
    astar_result = a_star_search(grid, start, goal)

    output_folder = Path(output_folder)
    bfs_image = draw_search(
        grid, start, goal, bfs_result,
        "BFS on the example grid", output_folder / "bfs_visualization.png",
    )
    astar_image = draw_search(
        grid, start, goal, astar_result,
        "A* on the example grid", output_folder / "astar_visualization.png",
    )
    comparison_image = save_comparison(
        bfs_result,
        astar_result,
        output_folder / "algorithm_comparison.png",
    )

    # Print the same useful numbers that appear in the comparison chart.
    for search_name, result in (("BFS", bfs_result), ("A*", astar_result)):
        print(f"{search_name}: path found = {result['found']}")
        print(f"{search_name}: explored cells = {len(result['explored'])}")
        print(f"{search_name}: path length = {result['path_length']}")
        print(f"{search_name}: path cost = {result['path_cost']}")

    print(f"Start: {start}; goal: {goal}")
    print(f"Saved: {bfs_image.resolve()}")
    print(f"Saved: {astar_image.resolve()}")
    print(f"Saved: {comparison_image.resolve()}")


def main():
    """Read optional settings from the terminal and start the example."""
    parser = argparse.ArgumentParser(
        description="Compare BFS and A* on a small grid map."
    )
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=Path(__file__).parent / "outputs",
        help="folder where the pictures will be saved",
    )
    arguments = parser.parse_args()
    run_demo(arguments.output_folder)


if __name__ == "__main__":
    main()
