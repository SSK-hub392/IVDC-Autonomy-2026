# PS2 - Motion Planning

## Section 1 - Path-planning fundamentals

### 1. What is the difference between a path and a trajectory?

A path is a list of places to go. A trajectory also says when to reach those places and may include speed and direction. The path planner in this project gives a path on a grid. It does not add time or vehicle speed.

### 2. What do waypoint, obstacle, free space, start state, and goal mean?

- A **waypoint** is a place along a path.
- An **obstacle** is a place the vehicle must avoid.
- **Free space** is a place the vehicle is allowed to use.
- The **start state** is where the trip begins. A real vehicle state may also include heading and speed.
- The **goal** is the place or condition the vehicle wants to reach.

## Section 2 - Environment representation

### 3. What is a 2D grid map?

A 2D grid map splits an area into rows and columns of cells. In this program, each cell is either free or an obstacle. The vehicle can move up, down, left, or right by one cell.

### 4. What is an occupancy grid?

An occupancy grid stores what is known about each cell. A cell can have an occupied chance rather than only a yes or no value. A robot can update those chances as it gets new sensor readings. This small program uses a known map and does not calculate chances.

### 5. What are free, occupied, and unknown cells?

A **free** cell is believed to be open. An **occupied** cell is believed to contain an obstacle. An **unknown** cell has not been seen or is still uncertain. The example grid has free and occupied cells, but no unknown cells.

## Section 3 - Search algorithms

### 6. How does Breadth-First Search (BFS) work?

BFS uses a first-in, first-out queue. It checks all cells one move from the start, then all cells two moves away, and continues in that order. It stores how each cell was reached so it can build the route back from the goal. If every move costs one, BFS finds a route with the fewest moves. For example, from a cell at row 0, column 0, it checks the open cells directly above, below, left, and right before checking cells two moves away. A cell is marked visited when it is added to the queue so it is not added again.

### 7. How does Dijkstra's Algorithm work, and how is it different from BFS?

Dijkstra keeps the total travel cost found so far for each cell. It always checks the cell with the lowest known cost next. This works when moves have different costs, as long as costs are not negative. BFS uses a simple queue and is enough when every move costs the same. The required demo compares BFS with A*, but Dijkstra is described here for the research questions.

### 8. How does A* use a heuristic?

A* gives each cell a priority: `f = g + h`. `g` is the cost from the start to this cell. `h` is an estimate from this cell to the goal. For a grid with up, down, left, and right moves, Manhattan distance is `abs(row difference) + abs(column difference)`. It points the search toward the goal. With equal step costs and this distance estimate, A* can find a shortest route while often checking fewer cells. It is not guaranteed to check fewer cells on every map.

### 9. How are BFS, Dijkstra, and A* different?

BFS is good for a map where every step costs the same. Dijkstra accounts for different step costs but does not use the goal's direction to guide the search. A* accounts for step cost and uses an estimate toward the goal. If every step costs one, Dijkstra and BFS can return a shortest path; A* can too when its estimate does not overstate the remaining cost.

## Section 4 - Global and local planning

### 10. What is the difference between a global path and a local motion decision?

A global path is a route across a larger map toward the destination. A local motion decision chooses what the vehicle should do near its current position, based on nearby space and movement limits. The grid program only makes a basic global route.

### 11. Why might a vehicle need to re-plan?

A new obstacle may block the old route or make it unsafe. The vehicle can update its map and search for another route. A real vehicle also needs to check that the new route can be followed safely while it is moving.

## References

- Amit Patel, Red Blob Games, [Introduction to the A* Algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html).
- Amit Patel, Red Blob Games, [A* Implementation](https://www.redblobgames.com/pathfinding/a-star/implementation.html).
