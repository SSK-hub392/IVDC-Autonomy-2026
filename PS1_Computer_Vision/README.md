# PS1 — Lane Detection

This program looks for the lane edges in one road photo. It saves a black-and-white lane mask plus pictures of the steps used to make it.

The sample road photo from the assignment is included at `PS1_Computer_Vision/images/provided_test_image.jpg`, so you can try the program before finding another image.

## Run the example

Open a terminal in the main project folder. Install the project libraries first by following the main [README](../README.md#install-the-libraries).

**Windows PowerShell:**

```powershell
.venv\Scripts\python.exe PS1_Computer_Vision\lane_detection.py PS1_Computer_Vision\images\provided_test_image.jpg
```

**macOS or Linux:**

```bash
.venv/bin/python PS1_Computer_Vision/lane_detection.py PS1_Computer_Vision/images/provided_test_image.jpg
```

The output pictures are saved to `PS1_Computer_Vision/outputs/`. To use a different photo, replace the image path in the command. To save to another folder, add `--output-folder folder_name` after the image path.

## How the code works

The functions in `lane_detection.py` each handle one part of the process. Read `process_image` first to see the steps in order, then open the helper function named beside each step.

1. **Load the photo.** `cv2.imread` opens the file. If it cannot open the path, the program prints an error. The image has a height, width, and colour values for each pixel.
2. **Simplify and smooth it.** `cv2.cvtColor` makes a grayscale image with brightness values. `cv2.GaussianBlur` smooths tiny changes that could look like edges.
3. **Find useful pixels.** `cv2.Canny` finds sharp brightness changes. The HSV colour masks separately look for white and yellow paint. The program combines these results so it can use both edge shape and paint colour.
4. **Limit the search to the road.** `make_road_mask` draws a trapezoid over the lower middle of the image. `cv2.bitwise_and` hides pixels outside the trapezoid.
5. **Find short line pieces.** `cv2.HoughLinesP` finds straight segments in the remaining pixels. `find_lane_points` sorts their end points into left and right groups using each segment's tilt and location.
6. **Extend the lane sides.** `fit_lane_boundary` uses `np.polyfit` to fit one long straight line through each group of points. If only one side is found, `estimate_missing_boundary` makes a rough guess for the other side using a chosen lane width.
7. **Draw and save the lane.** `make_lane_polygon` makes a four-corner shape between the two lines. Filling it with 0 on a white image creates the assignment's black-lane, white-background bitmap. The program also draws a green region and red lines on the colour photo.

## Saved pictures

| File | What to look for |
| --- | --- |
| `01_grayscale.png` | The photo represented by brightness only. |
| `02_blurred.png` | The grayscale photo after smoothing. |
| `03_colour_mask.png` | Pixels that look white or yellow. |
| `04_edges.png` | Sharp brightness changes found by Canny. |
| `05_roi_mask.png` | The trapezoid that marks the road search area. |
| `06_roi_edges.png` | Edge and paint pixels kept inside the road area. |
| `07_detected_lane_boundaries.png` | The original photo with red boundaries and a green lane region. |
| `08_lane_region_binary.png` | The requested black lane region on a white background. |

## Things to experiment with

Change one value at a time, run the program again, and compare the saved pictures:

- The two numbers in `cv2.Canny(blurred, 50, 150)` change how strong an edge must be before it is kept.
- The number ranges in `white_mask` and `yellow_mask` decide which colours count as paint.
- The four corner positions in `make_road_mask` change where the road search area sits.
- `threshold`, `minLineLength`, and `maxLineGap` in `cv2.HoughLinesP` affect how line segments are found.

The numbers are starting points for the sample camera view, not universal values. A different image may need different settings.

## Limits

This is a straight-line example, not a road-understanding system. It can mistake shadows or road seams for lane paint, and curves or unusual camera angles can cause poor results. If a side is estimated, that side is a guess based on lane width. The assignment asks for an understandable method and intermediate images; it does not require a pretrained model, and this program does not use one.
