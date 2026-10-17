# PS2 - Motion Planning

## Section 1 - Path-planning basics

### 1. What is the difference between a path and a trajectory?

A path is a list of places to visit. A trajectory also says when to reach them and may include speed. This program finds a path on a grid.

### 2. What do waypoint, obstacle, free space, start state, and goal mean?

- A **waypoint** is a place along the route.
- An **obstacle** is an area to avoid.
- **Free space** is an area the vehicle can use.
- The **start state** is where the trip begins.
- The **goal** is where the trip should end.

## Section 2 - Map representation

### 3. What is a 2D grid map?

A grid map divides an area into rows and columns. Each cell in this program is free or blocked. The search can move one cell up, down, left, or right.

### 4. What is an occupancy grid?

An occupancy grid records whether places are free, blocked, or not yet known. A robot can update its map from sensor readings. This program uses a fixed map.

### 5. What are free, occupied, and unknown cells?

A **free** cell can be used. An **occupied** cell has an obstacle. An **unknown** cell has not been checked yet. The example map has free and occupied cells.

## Section 3 - Search algorithms

### 6. How does Breadth-First Search (BFS) work?

BFS uses a first-in, first-out queue. It checks nearby cells first, then cells farther away. It marks a cell visited when it is added to the queue. If every move has the same cost, BFS finds a path with the fewest moves.

### 7. How does Dijkstra's Algorithm work, and how is it different from BFS?

Dijkstra checks the cell with the lowest known travel cost first. It can handle different non-negative move costs. BFS is simpler when every move costs the same.

### 8. How does A* use a heuristic?

A* gives each cell a score: `f = g + h`. `g` is the cost from the start. `h` estimates the cost to the goal. On a four-direction grid, Manhattan distance is a simple estimate. A* can find a shortest path when the estimate does not overstate the remaining cost.

### 9. How are BFS, Dijkstra, and A* different?

BFS is for equal-cost moves. Dijkstra handles different move costs. A* also uses an estimate to guide its search toward the goal. With equal-cost grid moves, BFS and A* can both find a shortest path.

## Section 4 - Global and local planning

### 10. What is the difference between a global path and a local motion decision?

A global path gives a route across a map. A local decision chooses what to do nearby, based on the space around the vehicle. This program makes a basic global path.

### 11. Why might a vehicle need to re-plan?

A new obstacle may block the route. The vehicle can update its map and search for another path. It must still check that the new path is safe to follow.

## References

- Amit Patel, Red Blob Games, [Introduction to the A* Algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html).
- Amit Patel, Red Blob Games, [A* Implementation](https://www.redblobgames.com/pathfinding/a-star/implementation.html).
