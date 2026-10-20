# IVDC Autonomy 2026

Beginner examples for two autonomous-vehicle topics: finding lane boundaries in a road photo (PS1) and finding a route through a grid map (PS2). The attached induction document also describes PS3, but this repository covers PS1 and PS2 only. These examples are for learning; they are not software for controlling a real vehicle.

## Project files

| Folder or file | Contents |
| --- | --- |
| `PS1_Computer_Vision/` | Lane detection code, the assignment's sample photo, explanations, and example outputs. |
| `PS2_Motion_Planning/` | BFS and A* code, explanations, and example outputs. |
| `requirements.txt` | Python libraries used by both programs. |
| `PS1_Computer_Vision/research.md`, `PS2_Motion_Planning/research.md` | Editable assignment answers. PDF copies are in the same folders. |

## Install

Use Python 3.10 or newer. Open PowerShell (Windows) or Terminal (macOS/Linux) in this folder, then create a project-only environment and install the libraries:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On macOS/Linux, use these commands instead:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Run a program

PS1 uses the sample road photo included in the repository. You can replace its path with another `.jpg` or `.png` photo.

```powershell
.venv\Scripts\python.exe PS1_Computer_Vision\lane_detection.py PS1_Computer_Vision\images\provided_test_image.jpg
.venv\Scripts\python.exe PS2_Motion_Planning\path_planning.py
```

On macOS/Linux:

```bash
.venv/bin/python PS1_Computer_Vision/lane_detection.py PS1_Computer_Vision/images/provided_test_image.jpg
.venv/bin/python PS2_Motion_Planning/path_planning.py
```

PS1 saves intermediate pictures and the required black-lane, white-background bitmap in `PS1_Computer_Vision/outputs/`. PS2 saves maps showing explored cells and routes, plus a BFS/A* comparison chart in `PS2_Motion_Planning/outputs/`. See each folder's README for a code walkthrough and ideas to experiment with.

## Run the included checks

```powershell
.venv\Scripts\python.exe -m unittest discover -s PS1_Computer_Vision\tests
.venv\Scripts\python.exe -m unittest discover -s PS2_Motion_Planning\tests
```

For macOS/Linux, replace `.venv\Scripts\python.exe` with `.venv/bin/python` and change the folder separators to `/`.

## Limits and acknowledgement

PS1 uses colour ranges and straight lines, so lighting, curves, worn paint, and camera angle can affect it. If one lane side is missing, it estimates that side. PS2 uses a small fixed grid, equal-cost moves, and four directions; its route is not a vehicle trajectory.

AI tools helped prepare parts of the code and beginner explanations and supported research. References are listed in the research documents.
