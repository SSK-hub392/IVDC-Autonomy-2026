"""Find approximate lane boundaries in one road image.

This beginner example follows a simple image-processing pipeline:
load -> grayscale/blur -> edges -> road mask -> line detection -> draw/save.
It uses straight lines, so it is meant for learning rather than real vehicle control.
"""

import argparse
from pathlib import Path

import cv2
import numpy as np


def make_output_folder(folder):
    """Create the output folder if it does not exist yet."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def save_image(path, image):
    """Save an image and explain clearly if saving did not work."""
    if not cv2.imwrite(str(path), image):
        raise OSError(f"Could not save image: {path}")


def make_road_mask(height, width):
    """Make a white trapezoid over the road and black everywhere else.

    OpenCV pixel coordinates start at the top-left. x goes right and y goes
    down. The trapezoid is only a rough guess, so it may need adjusting for
    a camera mounted in a different place.
    """
    mask = np.zeros((height, width), dtype=np.uint8)

    top_y = int(height * 0.55)
    road_corners = np.array([[
        (int(width * 0.05), height - 1),  # bottom-left
        (int(width * 0.15), top_y),      # top-left
        (int(width * 0.85), top_y),      # top-right
        (int(width * 0.95), height - 1), # bottom-right
    ]], dtype=np.int32)

    # Fill the road area with 255 (white). The rest of the mask stays 0 (black).
    cv2.fillPoly(mask, road_corners, 255)
    return mask


def find_lane_points(edge_image, width):
    """Find short line segments and group their end points by road side."""
    # HoughLinesP finds straight line segments from white pixels in edge_image.
    # The size-based values work across different image widths.
    line_segments = cv2.HoughLinesP(
        edge_image,
        rho=1,
        theta=np.pi / 180,
        threshold=max(20, int(width * 0.03)),
        minLineLength=max(18, int(width * 0.04)),
        maxLineGap=max(12, int(width * 0.03)),
    )

    left_points = []
    right_points = []

    # OpenCV returns None when it did not find any lines.
    if line_segments is None:
        return left_points, right_points

    for segment in line_segments:
        x1, y1, x2, y2 = segment[0]

        # Compare horizontal movement (change_x) with vertical movement
        # (change_y). This direction value tells us which way a segment tilts.
        change_x = x2 - x1
        change_y = y2 - y1

        # A nearly horizontal line is unlikely to be a lane boundary.
        if abs(change_y) < 5:
            continue

        direction = change_x / change_y
        middle_x = (x1 + x2) / 2
        segment_points = [(x1, y1), (x2, y2)]

        # Lane lines on the left and right usually tilt in opposite directions.
        if direction < -0.18 and middle_x < width / 2:
            left_points.extend(segment_points)
        elif direction > 0.18 and middle_x > width / 2:
            right_points.extend(segment_points)

    return left_points, right_points


def fit_lane_boundary(points, height, width):
    """Fit one long boundary through many short-line points.

    Return two points: one near the top of the road and one at the image
    bottom. Return None if there are not enough useful points.
    """
    if len(points) < 4:
        return None

    point_array = np.asarray(points, dtype=np.float32)

    # polyfit needs at least two different y values to find a line.
    if len(np.unique(point_array[:, 1])) < 2:
        return None

    # Fit x from y: y is the vertical axis, and x tells us where the lane is.
    x_change_per_y, x_at_y_zero = np.polyfit(
        point_array[:, 1], point_array[:, 0], 1
    )

    top_y = int(height * 0.55)
    bottom_y = height - 1

    top_x = int(x_change_per_y * top_y + x_at_y_zero)
    bottom_x = int(x_change_per_y * bottom_y + x_at_y_zero)

    # Keep both x-coordinates inside the image.
    top_x = int(np.clip(top_x, 0, width - 1))
    bottom_x = int(np.clip(bottom_x, 0, width - 1))

    return (top_x, top_y), (bottom_x, bottom_y)


def estimate_missing_boundary(found_boundary, missing_side, width):
    """Roughly guess one side if the image only showed the other side."""
    top_lane_width = int(width * 0.28)
    bottom_lane_width = int(width * 0.55)

    # The left boundary is to the left of the right one, and vice versa.
    if missing_side == "left":
        direction = -1
    else:
        direction = 1

    top_point, bottom_point = found_boundary
    guessed_top_x = top_point[0] + direction * top_lane_width
    guessed_bottom_x = bottom_point[0] + direction * bottom_lane_width

    guessed_top = (int(np.clip(guessed_top_x, 0, width - 1)), top_point[1])
    guessed_bottom = (int(np.clip(guessed_bottom_x, 0, width - 1)), bottom_point[1])
    return guessed_top, guessed_bottom


def make_lane_polygon(left_boundary, right_boundary):
    """Return the four corners between the two lane boundaries."""
    left_top, left_bottom = left_boundary
    right_top, right_bottom = right_boundary

    # Going around the shape in order makes a closed lane-area polygon.
    return np.array([[
        left_bottom,
        left_top,
        right_top,
        right_bottom,
    ]], dtype=np.int32)


def process_image(image_path, output_folder):
    """Run all lane-detection steps and save their images."""
    image_path = Path(image_path)
    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(
            f"Could not open image: {image_path}. Check the file name and path."
        )

    output_folder = make_output_folder(output_folder)
    height, width = image.shape[:2]

    # Convert the colour image to brightness only, then smooth small details.
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)

    # Look for sharp brightness changes. These often include lane markings.
    edges = cv2.Canny(blurred, 50, 150)

    # Also look for white and yellow paint by its colour.
    # HSV separates colour (hue) from brightness, which helps make colour ranges.
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(
        hsv_image,
        np.array([0, 0, 170]),
        np.array([180, 90, 255]),
    )
    yellow_mask = cv2.inRange(
        hsv_image,
        np.array([12, 55, 90]),
        np.array([40, 255, 255]),
    )
    colour_mask = cv2.bitwise_or(white_mask, yellow_mask)

    # Keep only the road-shaped part of both the edge and colour images.
    road_mask = make_road_mask(height, width)
    road_edges = cv2.bitwise_and(edges, road_mask)
    road_colour = cv2.bitwise_and(colour_mask, road_mask)
    combined_road_features = cv2.bitwise_or(road_edges, road_colour)

    # Find short line pieces, then fit one longer line for each side.
    left_points, right_points = find_lane_points(combined_road_features, width)
    left_boundary = fit_lane_boundary(left_points, height, width)
    right_boundary = fit_lane_boundary(right_points, height, width)

    # Remember which sides were actually found before estimating any missing side.
    left_was_detected = left_boundary is not None
    right_was_detected = right_boundary is not None

    # Save intermediate images so a beginner can inspect each pipeline step.
    save_image(output_folder / "01_grayscale.png", grayscale)
    save_image(output_folder / "02_blurred.png", blurred)
    save_image(output_folder / "03_colour_mask.png", colour_mask)
    save_image(output_folder / "04_edges.png", edges)
    save_image(output_folder / "05_roi_mask.png", road_mask)
    save_image(output_folder / "06_roi_edges.png", combined_road_features)

    if left_boundary is None and right_boundary is None:
        raise RuntimeError(
            f"No lane boundary was found. Check the saved step images in {output_folder.resolve()}"
        )

    # If one boundary is missing, estimate it from the one that was detected.
    if left_boundary is None:
        left_boundary = estimate_missing_boundary(right_boundary, "left", width)
    if right_boundary is None:
        right_boundary = estimate_missing_boundary(left_boundary, "right", width)

    lane_polygon = make_lane_polygon(left_boundary, right_boundary)

    # The final black-and-white result uses black inside the lane and white outside.
    binary_mask = np.full((height, width), 255, dtype=np.uint8)
    cv2.fillPoly(binary_mask, lane_polygon, 0)

    # Blend a green lane area over the original photo, then draw red boundaries.
    overlay = image.copy()
    lane_colour = np.zeros_like(image)
    cv2.fillPoly(lane_colour, lane_polygon, (40, 170, 40))
    overlay = cv2.addWeighted(overlay, 0.72, lane_colour, 0.28, 0)

    line_thickness = max(2, width // 300)
    cv2.line(overlay, left_boundary[0], left_boundary[1], (0, 0, 255), line_thickness)
    cv2.line(overlay, right_boundary[0], right_boundary[1], (0, 0, 255), line_thickness)

    save_image(output_folder / "07_detected_lane_boundaries.png", overlay)
    save_image(output_folder / "08_lane_region_binary.png", binary_mask)

    # Print a short report. An estimated boundary is a guess, not a detection.
    summary = {
        "left_detected": left_was_detected,
        "right_detected": right_was_detected,
        "left_estimated": not left_was_detected,
        "right_estimated": not right_was_detected,
        "output_folder": output_folder.resolve(),
        "binary_path": (output_folder / "08_lane_region_binary.png").resolve(),
    }
    for name, value in summary.items():
        print(f"{name}: {value}")

    return summary


def main():
    """Read the image path typed after the script name in the terminal."""
    parser = argparse.ArgumentParser(
        description="Find approximate lane boundaries in a road image."
    )
    parser.add_argument("image", type=Path, help="path to a road image")
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=Path(__file__).parent / "outputs",
        help="folder where the result images will be saved",
    )

    arguments = parser.parse_args()

    try:
        process_image(arguments.image, arguments.output_folder)
    except (FileNotFoundError, OSError, RuntimeError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
