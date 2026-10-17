import sys
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
test_temp_folder = Path(__file__).resolve().parents[1] / "outputs" / ".test_temp"
test_temp_folder.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(test_temp_folder)
from lane_detection import process_image


def make_road_image(include_right=True):
    image = np.zeros((480, 800, 3), dtype=np.uint8)
    image[:] = (55, 115, 55)
    road = np.array([[270, 170], [530, 170], [790, 479], [10, 479]], dtype=np.int32)
    cv2.fillPoly(image, [road], (70, 70, 70))
    cv2.line(image, (270, 170), (10, 479), (245, 245, 245), 12)
    if include_right:
        cv2.line(image, (530, 170), (790, 479), (0, 220, 255), 12)
    return image


class LaneDetectionTests(unittest.TestCase):
    def test_two_markings_make_black_inside_and_white_outside(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            input_path = root / "road.png"
            cv2.imwrite(str(input_path), make_road_image())
            result = process_image(input_path, root / "results")
            output = cv2.imread(str(result["binary_path"]), cv2.IMREAD_GRAYSCALE)
            self.assertTrue(result["left_detected"])
            self.assertTrue(result["right_detected"])
            self.assertIn(0, np.unique(output))
            self.assertIn(255, np.unique(output))
            self.assertEqual(output.shape, (480, 800))

    def test_missing_marking_is_reported_as_estimated(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            input_path = root / "one_marking.png"
            cv2.imwrite(str(input_path), make_road_image(include_right=False))
            result = process_image(input_path, root / "results")
            self.assertTrue(result["left_detected"])
            self.assertTrue(result["right_estimated"])
            self.assertFalse(result["right_detected"])

    def test_missing_image_has_clear_error(self):
        with tempfile.TemporaryDirectory() as folder:
            missing_path = Path(folder) / "missing.png"
            with self.assertRaisesRegex(FileNotFoundError, "Could not open image"):
                process_image(missing_path, Path(folder) / "results")

    def test_no_lane_marks_saves_steps_then_stops(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            input_path = root / "blank.png"
            cv2.imwrite(str(input_path), np.zeros((480, 800, 3), dtype=np.uint8))
            with self.assertRaisesRegex(RuntimeError, "No lane boundary was found"):
                process_image(input_path, root / "results")
            self.assertTrue((root / "results" / "04_edges.png").exists())


if __name__ == "__main__":
    unittest.main()
