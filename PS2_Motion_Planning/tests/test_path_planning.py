import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_planning import a_star_search, breadth_first_search, build_default_grid


def check_path(test_case, grid, path, start, goal):
    test_case.assertEqual(path[0], start)
    test_case.assertEqual(path[-1], goal)
    for row, column in path:
        test_case.assertEqual(grid[row, column], 0)
    for first, second in zip(path, path[1:]):
        test_case.assertEqual(abs(first[0] - second[0]) + abs(first[1] - second[1]), 1)


class PathPlanningTests(unittest.TestCase):
    def test_default_grid_has_connected_path_and_avoids_obstacles(self):
        grid = build_default_grid()
        start, goal = (1, 1), (16, 24)
        for search in (breadth_first_search, a_star_search):
            result = search(grid, start, goal)
            self.assertTrue(result["found"])
            check_path(self, grid, result["path"], start, goal)

    def test_obstacle_forces_a_detour_and_both_searches_find_shortest_length(self):
        grid = np.zeros((5, 5), dtype=np.uint8)
        grid[1:4, 2] = 1
        start, goal = (2, 0), (2, 4)
        bfs_result = breadth_first_search(grid, start, goal)
        astar_result = a_star_search(grid, start, goal)
        self.assertGreater(bfs_result["path_length"], 4)
        self.assertEqual(bfs_result["path_length"], astar_result["path_length"])
        check_path(self, grid, astar_result["path"], start, goal)

    def test_unreachable_goal_returns_no_path(self):
        grid = np.zeros((3, 3), dtype=np.uint8)
        grid[:, 1] = 1
        result = a_star_search(grid, (1, 0), (1, 2))
        self.assertFalse(result["found"])
        self.assertEqual(result["path"], [])

    def test_adjacent_start_and_goal(self):
        grid = np.zeros((2, 2), dtype=np.uint8)
        result = a_star_search(grid, (0, 0), (0, 1))
        self.assertTrue(result["found"])
        self.assertEqual(result["path"], [(0, 0), (0, 1)])

    def test_invalid_start_or_goal_is_rejected(self):
        grid = np.zeros((3, 3), dtype=np.uint8)
        with self.assertRaises(ValueError):
            a_star_search(grid, (-1, 0), (2, 2))
        with self.assertRaises(ValueError):
            breadth_first_search(grid, (0, 0), (3, 2))
        grid[1, 1] = 1
        with self.assertRaises(ValueError):
            a_star_search(grid, (0, 0), (1, 1))


if __name__ == "__main__":
    unittest.main()
