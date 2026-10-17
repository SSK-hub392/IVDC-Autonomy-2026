# PS1 - Computer Vision

## Task

Read a road image and make a black-and-white image. The area between the estimated lane sides is black. Everything outside it is white. The program also saves pictures from the steps that led to the result.

## Approach

The program makes a grayscale image and a blurred image. Blur reduces small texture before Canny edge detection. It also makes an HSV colour mask for white and yellow paint. A trapezoid ROI keeps the search near the road. Hough line segments are grouped by their direction and image side, then fitted to two lines. If one line is missing, the program estimates that side from the line it found and reports that it was estimated.

The final mask is made from the area between the two lines. It is not an object detector and does not understand what a road is.

## Install and run

Install the project dependencies from the project root as described in the main README. From the project root, run:

```powershell
.venv\Scripts\python.exe PS1_Computer_Vision\lane_detection.py path\to\road_image.jpg
```

Choose another output folder with:

```powershell
.venv\Scripts\python.exe PS1_Computer_Vision\lane_detection.py path\to\road_image.jpg --output-folder PS1_Computer_Vision\outputs\my_run
```

If the file cannot be opened, the program prints the missing path and asks for a valid image path. No real test image was available when this package was made. The saved `synthetic_road.png` is an artificial example created for checking the code.

## Outputs

The program saves grayscale, blurred, colour mask, edge, ROI, ROI edge, lane overlay, and final bitmap images. The final bitmap filename is `08_lane_region_binary.png`. The code prints the output folder and whether each boundary was detected or estimated.

## Libraries

OpenCV loads and processes images. NumPy stores and combines image arrays. Install all project libraries with `python -m pip install -r requirements.txt` from the project root.

## Limitations

This is a simple straight-line method. A curve may not fit one line. Fixed colour ranges may fail in shade, glare, or on another camera. Road seams may look like paint. If both boundaries are missing, the program saves intermediate pictures and stops without making a false final result. If one side is missing, the other side is estimated from a chosen lane width, so the result is only a rough guess.
