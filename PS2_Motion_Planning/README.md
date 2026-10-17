# PS2 - Motion Planning

## Task and map

The program finds a route from a start cell to a goal cell while avoiding blocked cells. In the NumPy grid, `0` means free and `1` means obstacle. The program only allows up, down, left, and right moves.

## Algorithms

BFS uses a queue and is a good choice when each move has the same cost. A* uses a priority queue. It adds the known number of moves so far to Manhattan distance, which estimates the remaining moves. Both searches store each cell's parent so the program can rebuild the route from the goal to the start. The search is written in this file; it does not use a path-finding library.

## Install and run

Install the project libraries from the project root, then run:

```powershell
.venv\Scripts\python.exe PS2_Motion_Planning\path_planning.py
```

The program prints whether each search found a path, the cells it explored, the path length and cost, and the start and goal. The default output folder is `PS2_Motion_Planning/outputs`.

## Outputs

- `bfs_visualization.png` shows BFS explored cells and its route.
- `astar_visualization.png` shows A* explored cells and its route.
- `algorithm_comparison.png` compares explored-cell counts and path lengths.

The figures use a legend for free cells, obstacles, explored cells, route, start, and goal.

## Tests and limits

The tests include a normal map, a forced detour, an unreachable goal, adjacent start and goal, and invalid positions. This grid does not model vehicle size, turning radius, speed, sensor uncertainty, or moving obstacles. A route on the grid is not yet a smooth vehicle trajectory.
