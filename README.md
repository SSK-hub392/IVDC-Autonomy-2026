# IVDC Autonomy 2026

This project is a study package for the three induction problems. It explains how a vehicle can see lane markings, plan a route on a map, and learn or control how it moves.

## Folders

```text
PS1_Computer_Vision/       lane program, answer source, PDF, tests, and images
PS2_Motion_Planning/       BFS and A* program, answer source, PDF, tests, and maps
PS3_Controllers_RL/        Q-learning program, answer source, PDF, tests, and plots
docs/                      notes about results and the separate Deep-ML project
```

The editable research answers are `PS1_Computer_Vision/research.md`, `PS2_Motion_Planning/research.md`, and `PS3_Controllers_RL/research.md`. The matching PDFs are [PS1 research](./PS1_Computer_Vision/research.pdf), [PS2 research](./PS2_Motion_Planning/research.pdf), and [PS3 research](./PS3_Controllers_RL/research.pdf).

## Software and setup

Use Python 3.10 or newer. In PowerShell, open this project folder and run:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The programs use NumPy and Matplotlib. PS1 also uses OpenCV.

## Run the programs

PS1 needs an image path. No real road test image was included with the assignment files available here.

```powershell
.venv\Scripts\python.exe PS1_Computer_Vision\lane_detection.py path\to\road_image.jpg
.venv\Scripts\python.exe PS2_Motion_Planning\path_planning.py
.venv\Scripts\python.exe PS3_Controllers_RL\q_learning_frozen_lake.py --episodes 5000 --seed 7
```

Each program saves images under its own `outputs` folder. PS1 saves the intermediate images and final black-inside, white-outside bitmap. PS2 saves separate BFS and A* views and a comparison chart. PS3 saves the training reward plot, learned policy view, and Q-table CSV.

## Run the checks

```powershell
.venv\Scripts\python.exe -m unittest discover -s PS1_Computer_Vision\tests
.venv\Scripts\python.exe -m unittest discover -s PS2_Motion_Planning\tests
.venv\Scripts\python.exe -m unittest discover -s PS3_Controllers_RL\tests
```

The tests use small artificial grids and images. They check image masks, lane fallback, valid and blocked paths, invalid positions, Q-table updates, terminal updates, repeatability, and the learned route. All 4 PS1 tests, 5 PS2 tests, and 7 PS3 tests passed in the preparation run. See `docs/limitations_and_observations.md` for the measured results and their limits.

## What each program does

- **PS1:** Uses colour ranges, Canny edges, a road-shaped ROI, and Hough line segments. It groups and fits left and right boundary lines. If one side is missing, it estimates that side and reports the estimate.
- **PS2:** Implements BFS and A* on a four-direction grid. A* uses Manhattan distance. Both algorithms use the same map and movement rules.
- **PS3:** Trains a small Q-table from scratch on a deterministic Frozen-Lake-style grid. It reports training and separate greedy evaluation results.

## Known limits and required student work

- PS1's included pictures are artificial examples. Run the program on the assigned road image when you have it. The fixed colour thresholds and straight-line fit can fail on curves, worn paint, shadows, or a different camera.
- PS2 is a small grid example. It does not model vehicle size, turning, speed, uncertainty, or moving obstacles.
- PS3's world is deterministic and small. Its measured success rate applies only to this map, seed, and run. It is not a road-driving controller.
- The Deep-ML project is separate from the local PS3 program. Follow `docs/deepml_guide.md`, finish the platform tasks, and capture the required proof yourself.

## AI and learning resources

OpenAI ChatGPT helped prepare an early draft of the explanations and code, which was then organized and checked in this package. This is AI-assisted study material, not a claim that the student wrote the first draft alone. OpenCV, Red Blob Games, MathWorks, and Hugging Face resources are listed in the three research documents. Please edit the explanations after studying them and only describe experiments you performed yourself.
