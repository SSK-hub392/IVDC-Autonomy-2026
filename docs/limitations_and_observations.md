# Results and limits

This file records the runs made while preparing this package. The images used for PS1 are artificial examples, not the assignment's missing road photograph.

## PS1

The program ran on a generated road image with two clear straight markings and on a second generated image with only the left marking. It saved each requested intermediate picture and a black-inside, white-outside bitmap. The second run reported the right boundary as estimated. A blank image caused the program to stop after saving its diagnostic images, and a missing input path returned a clear error. These checks do not measure performance on a real road image. All 4 PS1 tests passed.

## PS2

The program ran on its included 18 by 26 grid from `(1, 1)` to `(16, 24)`. BFS and A* both found a 38-move path. BFS explored 384 cells and A* explored 304 cells on this map. These counts depend on neighbour order and this map. The tests checked obstacles, no-path cases, adjacency, and invalid positions; all 5 passed.

## PS3

The program trained a new Q-table for 5,000 episodes with seed 7. The last 100 training episodes had a 96% goal rate. In a separate evaluation, the greedy policy reached the goal in 100 out of 100 episodes. The tests checked table size, valid actions, value updates, terminal updates, goal-reaching, the step limit, invalid settings, and repeatability; all 7 passed. The evaluation uses the same deterministic map on each attempt, so these repeated episodes are not independent tests of different road conditions. The result does not mean the agent will work on another map.

## Not done

- The assigned real PS1 road image was not present. Run the program on that image and write down what it detects and where it fails.
- Changes in real lighting and a real-road drivable-area mask were not tested.
- The external Deep-ML project and its screenshot are still the student's task.
