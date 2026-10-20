"""Find approximate lane boundaries in one road image."""

import argparse
from pathlib import Path

import cv2
import numpy as np


def save_image(path, image):
    """Save an image, and report a clear error if saving fails."""
    if not cv2.imwrite(str(path), image):
        raise OSError(f"Could not save image: {path}")


def make_road_mask(height, width):
    """Make a white trapezoid over the road; pixels outside it stay black."""
    mask = np.zeros((height, width), dtype=np.uint8)
    top_y = int(height * 0.55)

    # Image coordinates start at the top-left: x goes right, y goes down.
    road_corners = np.array([[
        (int(width * 0.05), height - 1),
        (int(width * 0.15), top_y),
        (int(width * 0.85), top_y),
        (int(width * 0.95), height - 1),
    ]], dtype=np.int32)
    cv2.fillPoly(mask, road_corners, 255)
    return mask


def find_lane_points(road_features, width):
    """Find short line pieces and group their points into left and right sides."""
    lines = cv2.HoughLinesP(
        road_features,
        rho=1,
        theta=np.pi / 180,
        threshold=max(20, int(width * 0.03)),
        minLineLength=max(18, int(width * 0.04)),
        maxLineGap=max(12, int(width * 0.03)),
    )

    left_points, right_points = [], []
    if lines is None:
        return left_points, right_points

    for line in lines:
        x1, y1, x2, y2 = line[0]
        change_x = x2 - x1
        change_y = y2 - y1
        if abs(change_y) < 5:  # Skip nearly horizontal lines.
            continue

        direction = change_x / change_y
        middle_x = (x1 + x2) / 2
        points = [(x1, y1), (x2, y2)]

        # Left and right lane lines usually tilt in opposite directions.
        if direction < -0.18 and middle_x < width / 2:
            left_points.extend(points)
        elif direction > 0.18 and middle_x > width / 2:
            right_points.extend(points)

    return left_points, right_points


def fit_lane_boundary(points, height, width):
    """Fit one long line through the detected points on a side of the lane."""
    if len(points) < 4:
        return None

    points = np.asarray(points, dtype=np.float32)
    if len(np.unique(points[:, 1])) < 2:
        return None

    # Fit x from y because y is the vertical image axis.
    slope, intercept = np.polyfit(points[:, 1], points[:, 0], 1)
    top_y = int(height * 0.55)
    bottom_y = height - 1

    top_x = int(np.clip(slope * top_y + intercept, 0, width - 1))
    bottom_x = int(np.clip(slope * bottom_y + intercept, 0, width - 1))
    return (top_x, top_y), (bottom_x, bottom_y)


def estimate_missing_boundary(found_boundary, missing_side, width):
    """Guess one side from the detected side using a simple lane-width estimate."""
    top, bottom = found_boundary
    direction = -1 if missing_side == "left" else 1

    top_x = top[0] + direction * int(width * 0.28)
    bottom_x = bottom[0] + direction * int(width * 0.55)
    guessed_top = (int(np.clip(top_x, 0, width - 1)), top[1])
    guessed_bottom = (int(np.clip(bottom_x, 0, width - 1)), bottom[1])
    return guessed_top, guessed_bottom


def process_image(image_path, output_folder):
    """Run the image steps, draw the lane area, and save the results."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Could not open image: {image_path}")

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    height, width = image.shape[:2]

    # 1. Prepare the image and find edges.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # 2. Find white and yellow paint using HSV colour ranges.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    white = cv2.inRange(hsv, np.array([0, 0, 170]), np.array([180, 90, 255]))
    yellow = cv2.inRange(hsv, np.array([12, 55, 90]), np.array([40, 255, 255]))
    colour_mask = cv2.bitwise_or(white, yellow)

    # 3. Keep edge and paint pixels only in the road-shaped area.
    road_mask = make_road_mask(height, width)
    road_edges = cv2.bitwise_and(edges, road_mask)
    road_colour = cv2.bitwise_and(colour_mask, road_mask)
    road_features = cv2.bitwise_or(road_edges, road_colour)

    # 4. Find short lines, group them, and fit one boundary per side.
    left_points, right_points = find_lane_points(road_features, width)
    left = fit_lane_boundary(left_points, height, width)
    right = fit_lane_boundary(right_points, height, width)
    left_detected = left is not None
    right_detected = right is not None

    # Save these steps even when no lane is found, so they can be inspected.
    steps = [
        ("01_grayscale.png", gray),
        ("02_blurred.png", blurred),
        ("03_colour_mask.png", colour_mask),
        ("04_edges.png", edges),
        ("05_roi_mask.png", road_mask),
        ("06_roi_edges.png", road_features),
    ]
    for filename, step_image in steps:
        save_image(output_folder / filename, step_image)

    if left is None and right is None:
        raise RuntimeError(f"No lane boundary was found. Check the images in {output_folder}")
    if left is None:
        left = estimate_missing_boundary(right, "left", width)
    if right is None:
        right = estimate_missing_boundary(left, "right", width)

    # The polygon is the area between the two lane boundaries.
    left_top, left_bottom = left
    right_top, right_bottom = right
    lane_polygon = np.array([[
        left_bottom, left_top, right_top, right_bottom
    ]], dtype=np.int32)

    # Assignment output: black inside the lane, white everywhere else.
    lane_mask = np.full((height, width), 255, dtype=np.uint8)
    cv2.fillPoly(lane_mask, lane_polygon, 0)

    # Also draw a green lane area and red boundary lines on the original photo.
    overlay = image.copy()
    green_area = np.zeros_like(image)
    cv2.fillPoly(green_area, lane_polygon, (40, 170, 40))
    overlay = cv2.addWeighted(overlay, 0.72, green_area, 0.28, 0)
    thickness = max(2, width // 300)
    cv2.line(overlay, left_top, left_bottom, (0, 0, 255), thickness)
    cv2.line(overlay, right_top, right_bottom, (0, 0, 255), thickness)

    save_image(output_folder / "07_detected_lane_boundaries.png", overlay)
    save_image(output_folder / "08_lane_region_binary.png", lane_mask)

    result = {
        "left_detected": left_detected,
        "right_detected": right_detected,
        "left_estimated": not left_detected,
        "right_estimated": not right_detected,
        "output_folder": output_folder.resolve(),
        "binary_path": (output_folder / "08_lane_region_binary.png").resolve(),
    }
    for name, value in result.items():
        print(f"{name}: {value}")
    return result


def main():
    """Read the image path from the command line and run the program."""
    parser = argparse.ArgumentParser(description="Find lane boundaries in a road image.")
    parser.add_argument("image", type=Path, help="path to a road image")
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=Path(__file__).parent / "outputs",
        help="folder for the result images",
    )
    args = parser.parse_args()

    try:
        process_image(args.image, args.output_folder)
    except (FileNotFoundError, OSError, RuntimeError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
