# IVDC Autonomy 2026

Within this repository I present my work for the three IVDC Autonomy 2026 problem statements. Throughout this project, I explore how an autonomous vehicle could identify lane markings, plan a route and learn how to navigate through reinforcement learning.

Each problem statement comes with its corresponding code, research answers, PDF, tests and output images. I have included instructions for running the prograns and reflections on their limitations.

## Project Structure

```

PS1_Computer_Vision/  Lane detection program, research answers, PDF, tests, and images

PS2_Motion_Planning/  BFS and A algorithms, research answers, PDF, tests, and maps

PS3_Controllers_RL/  Q-learning program, research answers, PDF, tests, and plots

docs/         Results, observations, and Deep-ML project guide

```

My Research answers are also available in editable markdown:

[PS1: Computer Vision](PS1_Computer_Vision/research.md)

[PS2: Motion Planning](PS2_Motion_Planning/research.md)

[PS3: Controllers and Reinforcement Learning](PS3_Controllers_RL/research.md)

And finally, the PDF versions of my Research can be found here:

[PS1 Research PDF](https://github.com/SSK-hub392/IVDC-Autonomy-2026/blob/main/PS1_Computer_Vision/research.pdf)

[PS2 Research PDF](https://github.com/SSK-hub392/IVDC-Autonomy-2026/blob/main/PS2_Motion_Planning/research.pdf)

[PS3 Research PDF](https://github.com/SSK-hub392/IVDC-Autonomy-2026/blob/main/PS3_Controllers_RL/research.pdf)

## Requirements

The programs will require Python version 3.10 or higher. This repository contains the following files for installing the required packages:

```

Open PowerShell in the project directory

Then run: python -m venv .venv

The run: .venv\Scripts\python.exe -m pip install -r requirements.txt

```

In addition to Python, the following libraries are also required:

- NumPy

- Matplotlib

- OpenCV (for the Vision task)

## How to Run the Programs

### PS1: Computer Vision

The lane detection program uses a supplied image of the road to detect the boundaries and save an image where the lane between the detected edges is black and everything else is white.

The original road testing input image was not supplied in the files for this project, so you will have to supply the image path when running the program.

To run the program:

```

.venv\Scripts\python.exe PS1_Computer_Vision\lane_detection.py path\to\road_image.jpg

```

It will save the various testing and output images to the 'outputs' directory in PS1.

### PS2: Motion Planning

This program will use the BFS and A algorithms to find the shortest path to a destination point while navigating around obstacles.

To run the program:

```

.venv\Scripts\python.exe PS2_Motion_Planning\path_planning.py

```

It will save the images representing the search and comparison to the 'outputs' directory in PS2.

### PS3: Reinforcement Learning

This program contains an implementation of the Q-learning algorithm to train an agent to navigate a small "Frozen Lake" style grid.

```

.venv\Scripts\python.exe PS3_Controllers_RL\q_learning_frozen_lake.py --episodes 5000 --seed 7

```

It will save a graphical representation, policy plot and Q-table to CSV as a result to the 'outputs' directory in PS3.

## How to Run the Tests

Each problem statements has its own set of tests:

For the PS1 tests:

```

.venv\Scripts\python.exe -m unittest discover -s PS1_Computer_Vision\tests

```

For the PS2 tests:

```

.venv\Scripts\python.exe -m unittest discover -s PS2_Motion_Planning\tests

```

And for the PS3 tests:

```

.venv\Scripts\python.exe -m unittest discover -s PS3_Controllers_RL\tests

```

When running the tests for the development phase, I saw that all 4 tests for PS1, 5 for PS2 and 7 for PS3 passed.

The tests use smaller images and grids, and test such aspects as the mask for the lanes, the pathfinding algorithms and whether they fail on blocked positions or incorrect inputs, and for Q-learning, the learning of the optimal path by the agent.

More information is available in `docs/limitations_and_observations.md`

## Implementation Overview

### PS1: Computer Vision

The lane detection program detects edges in road images using colour filtering, Canny-edge detection, a ROI mask, and the Hough transform to identify potential edges.

The program then selects the left and right boundaries as reference and calculates a binary image based on those, if it cannot detect one of the boundaries, it tries to estimate the other boundary from the remaining information.

### PS2: Motion Planning

The motion planning program implements BFS and A from scratch.

They both find a navigable path to a target location on a grid that has "obstacles", where A uses Manhattan-distance as its heuristic to navigate towards the target.

It visualizes the difference between the two algorithms in the path-finding process.

### PS3: Controllers and Reinforcement Learning

The PS3 implementation focuses on the Q-learning algorithm. It involves training an agent to navigate through a "Frozen Lake" grid by rewarding some actions and penalizing others.

This program's implementation focuses on the process of determining the policy based on a trained Q-table.

The process is visualized and saved as several graphs and CSV files for analysis on how it learned.

This local implementation serves as a demonstrator for the Q-learning methodology and not a real-world navigation controller for a self-driving vehicle.

## Limitations and Further Work

Each program has its own set of limitations to consider.

PS1: The images provided are fabricated examples and must still be tested on the actual road image provided for the problem statement. I have implemented a basic colour-based thresholding and detection of straight lines for the lanes but not for all road conditions, such as bends, faded lines, shadows, and poor visibility.

PS2: The motion planning program works with simple square grids and has no scale. The algorithm is unable to account for such variables as vehicle size, turning radius, speed, inaccuracy and moving obstacles.

PS3: The Q-learning implementation uses a relatively small deterministic environment. The results depend significantly on the map, random seed, and training parameters. Success in this environment is not necessarily representative of the ability of such a reinforcement learner to be able to control a vehicle.

The external Deep-ML project for PS3 is a separate part of the problem statement. Finishing the local implementation for PS3 does NOT finish that particular platform component. The completion instructions and further steps are discussed in `docs/depthml_guide.md`, including the fact that I still need to finish the various tests in the "Reinforcement Learning" section and capture the final screenshot once I have passed them.

## References and Human Review of AI Usage

I used OpenAi's ChatGPT to help brainstorm an initial set of explanations and code prior to actually working through the problem statements. I have since structured everything according to the guidelines and tested it out as part of the preparation for this submission.

The research section also contains pointers to the various web sources for the OpenCV, Red Blob Games, MathWorks and HuggingFace Deep RL course which are good resources for understanding the core concepts involved in this project.



