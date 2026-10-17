import argparse
from pathlib import Path

import cv2
import numpy as np


def make_output_folder(output_folder):
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder


def save_image(path, image):
    if not cv2.imwrite(str(path), image):
        raise OSError(f"Could not save image: {path}")


def build_roi(height, width):
    mask = np.zeros((height, width), dtype=np.uint8)
    top_y = int(height * 0.55)
    points = np.array([[
        (int(width * 0.05), height - 1),
        (int(width * 0.15), top_y),
        (int(width * 0.85), top_y),
        (int(width * 0.95), height - 1),
    ]], dtype=np.int32)
    cv2.fillPoly(mask, points, 255)
    return mask


def collect_line_points(edge_image, width, height):
    lines = cv2.HoughLinesP(
        edge_image,
        rho=1,
        theta=np.pi / 180,
        threshold=max(20, int(width * 0.03)),
        minLineLength=max(18, int(width * 0.04)),
        maxLineGap=max(12, int(width * 0.03)),
    )
    left_points = []
    right_points = []
    if lines is None:
        return left_points, right_points
    for x1, y1, x2, y2 in np.asarray(lines).reshape(-1, 4):
        change_y = y2 - y1
        change_x = x2 - x1
        if abs(change_y) < 5:
            continue
        sideways_per_down = change_x / change_y
        middle_x = (x1 + x2) / 2
        points = [(x1, y1), (x2, y2)]
        if sideways_per_down < -0.18 and middle_x < width / 2:
            left_points.extend(points)
        elif sideways_per_down > 0.18 and middle_x > width / 2:
            right_points.extend(points)
    return left_points, right_points


def fit_boundary(points, height, width):
    if len(points) < 4:
        return None
    point_array = np.asarray(points, dtype=np.float32)
    if len(np.unique(point_array[:, 1])) < 2:
        return None
    sideways_per_down, intercept = np.polyfit(point_array[:, 1], point_array[:, 0], 1)
    upper_y = int(height * 0.55)
    lower_y = height - 1
    upper_x = int(np.clip(sideways_per_down * upper_y + intercept, 0, width - 1))
    lower_x = int(np.clip(sideways_per_down * lower_y + intercept, 0, width - 1))
    return ((upper_x, upper_y), (lower_x, lower_y))


def estimate_missing_boundary(boundary, side, width):
    upper_width = int(width * 0.28)
    lower_width = int(width * 0.55)
    direction = -1 if side == "left" else 1
    upper, lower = boundary
    estimated_upper = (int(np.clip(upper[0] + direction * upper_width, 0, width - 1)), upper[1])
    estimated_lower = (int(np.clip(lower[0] + direction * lower_width, 0, width - 1)), lower[1])
    return estimated_upper, estimated_lower


def make_lane_polygon(left_boundary, right_boundary):
    return np.array([[
        left_boundary[1],
        left_boundary[0],
        right_boundary[0],
        right_boundary[1],
    ]], dtype=np.int32)


def process_image(image_path, output_folder):
    image_path = Path(image_path)
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(
            f"Could not open image: {image_path}. Give the path to a road image when you run this program."
        )
    output_folder = make_output_folder(output_folder)
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, np.array([0, 0, 170]), np.array([180, 90, 255]))
    yellow_mask = cv2.inRange(hsv, np.array([12, 55, 90]), np.array([40, 255, 255]))
    colour_mask = cv2.bitwise_or(white_mask, yellow_mask)
    edges = cv2.Canny(blurred, 50, 150)
    roi_mask = build_roi(height, width)
    roi_edges = cv2.bitwise_and(edges, roi_mask)
    roi_colour = cv2.bitwise_and(colour_mask, roi_mask)
    combined_edges = cv2.bitwise_or(roi_edges, roi_colour)
    left_points, right_points = collect_line_points(combined_edges, width, height)
    left_boundary = fit_boundary(left_points, height, width)
    right_boundary = fit_boundary(right_points, height, width)
    left_was_detected = left_boundary is not None
    right_was_detected = right_boundary is not None

    save_image(output_folder / "01_grayscale.png", gray)
    save_image(output_folder / "02_blurred.png", blurred)
    save_image(output_folder / "03_colour_mask.png", colour_mask)
    save_image(output_folder / "04_edges.png", edges)
    save_image(output_folder / "05_roi_mask.png", roi_mask)
    save_image(output_folder / "06_roi_edges.png", combined_edges)

    if left_boundary is None and right_boundary is None:
        raise RuntimeError(
            f"No lane boundary was found. Intermediate images were saved to {output_folder.resolve()}"
        )
    if left_boundary is None:
        left_boundary = estimate_missing_boundary(right_boundary, "left", width)
    if right_boundary is None:
        right_boundary = estimate_missing_boundary(left_boundary, "right", width)

    lane_polygon = make_lane_polygon(left_boundary, right_boundary)
    binary_mask = np.full((height, width), 255, dtype=np.uint8)
    cv2.fillPoly(binary_mask, lane_polygon, 0)
    overlay = image.copy()
    lane_colour = np.zeros_like(image)
    cv2.fillPoly(lane_colour, lane_polygon, (40, 170, 40))
    overlay = cv2.addWeighted(overlay, 0.72, lane_colour, 0.28, 0)
    cv2.line(overlay, left_boundary[0], left_boundary[1], (0, 0, 255), max(2, width // 300))
    cv2.line(overlay, right_boundary[0], right_boundary[1], (0, 0, 255), max(2, width // 300))
    save_image(output_folder / "07_detected_lane_boundaries.png", overlay)
    save_image(output_folder / "08_lane_region_binary.png", binary_mask)
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
    parser = argparse.ArgumentParser(description="Find lane boundaries in a road image.")
    parser.add_argument("image", type=Path, help="path to the input road image")
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=Path(__file__).parent / "outputs",
        help="folder for intermediate images and the final bitmap",
    )
    args = parser.parse_args()
    try:
        process_image(args.image, args.output_folder)
    except (FileNotFoundError, OSError, RuntimeError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
