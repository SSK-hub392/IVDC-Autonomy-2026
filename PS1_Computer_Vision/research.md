# PS1 - Computer Vision

## Gate 1 - How does a computer see?

### 1. What is a digital image?

A digital image is a grid of pixels. Each pixel stores a colour or brightness value. Resolution is the number of pixels across and down. A grayscale image is a 2D grid; a colour image stores three values for each pixel.

### 2. What are RGB and grayscale images?

RGB stores red, green, and blue values. Grayscale stores one brightness value. Colour can help find yellow or white lane paint. Grayscale can make edge detection simpler. Lighting can affect both.

## Gate 2 - Basic image processing

### 3. What is Gaussian blur, and why is it useful?

Gaussian blur smooths an image by averaging nearby pixels. It can reduce small noise before edge detection. Too much blur can hide lane markings.

### 4. What is HSV colour space?

HSV describes colour with hue, saturation, and brightness. A program can use colour ranges to find lane paint. Shadows and poor lighting can still cause errors.

### 5. What does Canny edge detection do?

Canny finds sharp brightness changes and marks them as edges. It cannot tell a lane marking from a shadow or road crack.

### 6. What is a Region of Interest (ROI)?

An ROI is the part of an image the program checks. For lane detection, it can cover the road near the bottom of the image and ignore much of the sky and buildings. Its shape depends on the camera view.

## Gate 3 - Detecting structure

### 7. What is a contour?

A contour is an outline around a connected shape in a binary image. It can show the shape's size and position, but it does not identify the object.

### 8. What is the Hough Transform?

The Hough line transform uses edge pixels to find likely straight lines. A lane program can group line segments on the left and right sides. Curved or broken lanes are harder to detect this way.

## Gate 4 - Lane and path perception

### 9. Why is lane or path detection useful?

It helps a vehicle estimate where it should drive. A planner can use this estimate to choose a route, and a controller can use it to steer.

### 10. Why can image conditions create false detections?

Shadows, cracks, and road texture can look like lane edges. Poor light or faded paint can hide real lanes. A basic program checks colour and shape, so it can mistake one for another.

### 11. Why is lane detection not enough for full autonomy?

Lane detection does not find every car, person, sign, or hazard. A vehicle also needs to understand its position, plan a safe route, control its motion, and check for danger.

## Gate 5 - Perspective and Bird's-Eye View

### 12. What is perspective distortion?

A camera turns the 3D road into a flat image. Far objects look smaller, and road edges may seem to meet. Image distances therefore do not directly show road distances.

### 13. What is a Bird's-Eye View (BEV)?

A BEV is a top-down view made from a road image. It can make lane position easier to compare. It depends on the camera view and works best when the road is fairly flat.

## References

- OpenCV, [Smoothing Images](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html).
- OpenCV, [Changing Colorspaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html).
- OpenCV, [Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html).
- OpenCV, [Hough Line Transform](https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html).
- OpenCV, [Contours](https://docs.opencv.org/4.x/d3/d05/tutorial_py_table_of_contents_contours.html).
- OpenCV, [Geometric Transformations](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html).
- OpenCV, [Getting Started with Images](https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html).
