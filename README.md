# IVDC Autonomy 2026

This repository contains simple Python examples and research answers for two IVDC Autonomy 2026 problem statements: lane detection and motion planning.

## Folders

```text
PS1_Computer_Vision/       lane detection program, research answer, PDF, tests, and example images
PS2_Motion_Planning/       BFS and A* program, research answer, PDF, tests, and grid maps
```

The editable research answers are in each problem statement folder. PDF copies are available for [PS1](./PS1_Computer_Vision/research.pdf) and [PS2](./PS2_Motion_Planning/research.pdf).

## Setup

Use Python 3.10 or newer. From this project folder, install the required packages:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Programs

PS1 accepts an image file as input. No real road test image was included with the assignment files available for this submission.

```powershell
.venv\Scripts\python.exe PS1_Computer_Vision\lane_detection.py path\to\road_image.jpg
.venv\Scripts\python.exe PS2_Motion_Planning\path_planning.py
```

The programs save their demonstration images in their own `outputs` folders. PS1 saves processing steps and a lane mask. PS2 saves the BFS and A* paths and a comparison chart.

## Checks

Run the included checks with:

```powershell
.venv\Scripts\python.exe -m unittest discover -s PS1_Computer_Vision\tests
.venv\Scripts\python.exe -m unittest discover -s PS2_Motion_Planning\tests
```

All 4 PS1 tests and 5 PS2 tests passed during preparation. The checks use generated images and a small grid map.

## Summary

- **PS1:** Uses colour thresholds, Canny edges, a region of interest, and Hough line segments to estimate lane boundaries.
- **PS2:** Compares breadth-first search (BFS) and A* on a four-direction grid. A* uses Manhattan distance.

## Limits

- PS1 was not checked on a real road image. Fixed colour thresholds and straight-line fitting may fail on curves, shadows, or worn lane markings.
- PS2 uses a small grid and does not model vehicle size, turning, speed, uncertainty, or moving obstacles.

## AI acknowledgement

AI tools helped with research, writing, and review of this submission. References are listed in the research documents.
