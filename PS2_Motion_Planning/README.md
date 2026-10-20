# PS2 — Grid Path Planning

This program compares two algorithms that find a route across a small map: breadth-first search (BFS) and A*. It shows the map, obstacles, start, goal, cells explored, and final route.

## Run the example

Open a terminal in the main project folder. Install the libraries by following the main [README](../README.md#install-the-libraries).

**Windows PowerShell:**

```powershell
.venv\Scripts\python.exe PS2_Motion_Planning\path_planning.py
```

**macOS or Linux:**

```bash
.venv/bin/python PS2_Motion_Planning/path_planning.py
```

The program prints a few results and saves three pictures in `PS2_Motion_Planning/outputs/`.

## Read the grid

`build_default_grid` creates the map as a NumPy array:

- `0` means a free cell the search may enter.
- `1` means an obstacle the search must avoid.
- A position such as `(1, 1)` means row 1, column 1. Rows count from the top; columns count from the left. Python starts counting at 0.
- `start` is where the route begins. `goal` is where it should finish.

The map is made of equal-sized cells. The search can move one cell up, down, left, or right. It cannot move diagonally.

## How the code works

Open `path_planning.py` and start with `run_demo` to see how the pieces connect. Then follow the steps below:

1. **Make the map and check positions.** `build_default_grid` creates open cells and obstacles. `check_position` makes sure the start and goal are inside the map and not on obstacles.
2. **Find possible next cells.** `get_neighbours` checks the four directions and returns only open cells that stay inside the map.
3. **Search the map.** `breadth_first_search` and `a_star_search` are the two search algorithms. Each remembers which cell led to the next one.
4. **Rebuild the route.** `make_result` starts at the goal and follows those remembered cells back to the start. It then reverses the list so the route reads from start to goal.
5. **Draw the results.** `draw_search` displays the map, explored cells, route, start, and goal. `save_comparison` makes a chart of the explored-cell counts and path lengths.

## BFS and A* in plain language

**BFS** uses a queue. A queue handles the oldest item first, so BFS checks all nearby cells before moving farther away. When every move costs one, the first route it finds uses the fewest moves.

**A*** uses a priority queue. It gives each cell a score:

```text
score = moves so far + estimated moves left
```

The estimate is the Manhattan distance: row steps plus column steps to the goal. It ignores obstacles while estimating, which makes it quick to calculate. In this four-direction example, BFS and A* find a shortest route, but A* often checks fewer cells.

The code implements both searches itself. It does not use a path-finding package.

## Saved pictures

- `bfs_visualization.png` shows BFS's explored cells and route.
- `astar_visualization.png` shows A*'s explored cells and route.
- `algorithm_comparison.png` compares how many cells each algorithm explored and the length of each route.

In the map pictures, light cells are free, dark cells are obstacles, blue cells were explored, the red line is the final route, the green circle is the start, and the purple star is the goal.

## Try changing the map

In `run_demo`, try changing the `start` and `goal` pairs. They must refer to free cells inside the grid.

In `build_default_grid`, change the `rows` or `columns` values to change the map size. The lines such as `grid[5:8, 3:20] = 1` add obstacles: the first range selects rows, and the second selects columns. Try changing or adding one obstacle block, then run the program again and compare the pictures.

## Limits

All moves in this example have the same cost, so it does not demonstrate Dijkstra's different-cost case. The grid does not model a vehicle's size, turning, speed, uncertain sensor readings, or moving obstacles. The output is a route through grid cells, not a smooth path that a car could follow directly.
