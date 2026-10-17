# PS1 - Computer Vision

## Gate 1 - How does a computer see?

### 1. What is a digital image?

A digital image is a grid of small picture parts called pixels. Each pixel stores a number for brightness or colour. Image resolution tells how many pixels wide and high the image is, such as 800 by 480. A grey image is a 2D table of numbers. A colour image is usually a table with three numbers at each pixel. OpenCV stores colour images in blue, green, red order by default.

### 2. What are RGB and grayscale images?

RGB stores red, green, and blue amounts for each pixel. Grayscale stores one brightness amount. Colour can help find yellow or white lane paint. Grayscale is simpler for finding edges. A road system may use both because each view can help with a different step. Shadows can change brightness, and camera settings can change colour, so neither view works perfectly in every scene.

## Gate 2 - Basic image processing

### 3. What is Gaussian blur, and why is it useful?

Gaussian blur replaces each pixel with a weighted average of nearby pixels. Pixels close by have more effect. This smooths small noise and road texture before edge detection. If the blur is too strong, it can also hide thin lane paint.

### 4. What is HSV colour space?

HSV stores colour as hue, saturation, and value (brightness). A colour filter can look for a hue range, such as yellow, without using all three RGB values at once. This can help find lane paint in some lighting. Strong shadows, glare, faded paint, and different cameras can still make the filter fail.

### 5. What does Canny edge detection do?

Canny finds places where image brightness changes quickly. It reduces noise, finds edge direction, keeps thin edge pixels, and uses two thresholds to keep strong edges and nearby weak edges. It returns an edge image. It cannot tell whether an edge is a lane, a shadow, or a crack.

### 6. What is a Region of Interest (ROI)?

An ROI is the part of an image that the program will study. A lane program may keep a trapezoid near the bottom of a forward road image. This leaves out much of the sky and buildings, which can reduce false line detections. The chosen shape depends on the camera angle and may need to change for another camera or road.

## Gate 3 - Detecting structure

### 7. What is a contour?

A contour is a line around the edge of a connected shape in a binary image. It can help measure the shape's area, length, position, and outer box. A contour does not name the object. Noise can create extra contours that do not matter.

### 8. What is the Hough Transform?

The Hough line transform uses edge pixels to vote for possible straight lines. A line with many votes is returned as a candidate. OpenCV's probabilistic version returns line segments. A lane program can group segments by their direction and image side. Curved lanes need more than one straight line, so this method is only an estimate.

## Gate 4 - Lane and path perception

### 9. Why is lane or path detection useful?

It helps a ground vehicle estimate the corridor it should stay in. A planner can use that estimate to choose a route, and a controller can use it to steer. The estimate should be checked over time because one image may be unclear.

### 10. Why can image conditions create false detections?

Shadows and road texture make brightness edges. Glare can hide lane paint. Poor light or worn markings can make paint hard to see. Signs, barriers, and road cracks can create lines that look like lanes. A basic image filter sees colour and shape; it does not know the meaning of each line.

### 11. Why is lane detection not enough for full autonomy?

Lane detection does not by itself find every car, person, sign, traffic light, or hazard. It does not decide who has right of way or how another road user may move. An autonomous vehicle also needs other perception, localization, planning, control, and safety checks.

## Gate 5 - Perspective and Bird's-Eye View

### 12. What is perspective distortion?

A camera turns a 3D scene into a flat image. Far objects look smaller, and parallel road edges can seem to meet in the distance. Pixel distances in the image are therefore not the same as distances on the road.

### 13. What is a Bird's-Eye View (BEV)?

A BEV is an estimated top-down view of the road. A perspective transform can make a flat road area look more like a map from above. This can make lane width and the vehicle's side-to-side position easier to compare. The result depends on camera calibration and the assumption that the road is flat. Hills and slopes can make it wrong.

## References

- OpenCV, [Smoothing Images](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html).
- OpenCV, [Changing Colorspaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html).
- OpenCV, [Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html).
- OpenCV, [Hough Line Transform](https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html).
- OpenCV, [Contours: Getting Started](https://docs.opencv.org/4.x/d3/d05/tutorial_py_table_of_contents_contours.html).
- OpenCV, [Geometric Transformations of Images](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html).
- OpenCV, [Getting Started with Images](https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html).
