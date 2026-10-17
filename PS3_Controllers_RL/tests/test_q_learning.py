import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from q_learning_frozen_lake import (
    FrozenLake,
    choose_action,
    evaluate_policy,
    follow_greedy_policy,
    train_agent,
    update_q_value,
    validate_parameters,
)


class QLearningTests(unittest.TestCase):
    def test_q_table_shape_and_action_range(self):
        environment = FrozenLake()
        q_table, _, _ = train_agent(environment, episodes=100, seed=4)
        self.assertEqual(q_table.shape, (16, 4))
        action = choose_action(q_table, environment.start_state, 1.0, np.random.default_rng(3))
        self.assertIn(action, range(4))

    def test_training_updates_q_values(self):
        environment = FrozenLake()
        q_table, _, _ = train_agent(environment, episodes=500, seed=7)
        self.assertTrue(np.any(q_table != 0))

    def test_terminal_update_does_not_add_future_value(self):
        q_table = np.zeros((16, 4))
        q_table[5] = 100
        update_q_value(q_table, 1, 2, -1.0, 5, True, 0.2, 0.9)
        self.assertAlmostEqual(q_table[1, 2], -0.2)

    def test_policy_reaches_goal_and_has_a_measured_success_rate(self):
        environment = FrozenLake()
        q_table, _, _ = train_agent(environment, episodes=5000, seed=7)
        route = follow_greedy_policy(environment, q_table, max_steps=60)
        evaluation = evaluate_policy(environment, q_table, episodes=25, max_steps=60)
        self.assertTrue(route["reached_goal"])
        self.assertEqual(evaluation["successes"], 25)
        self.assertEqual(evaluation["success_rate"], 1.0)

    def test_same_seed_gives_same_training_results(self):
        first = train_agent(FrozenLake(), episodes=300, seed=12)
        second = train_agent(FrozenLake(), episodes=300, seed=12)
        np.testing.assert_array_equal(first[0], second[0])
        np.testing.assert_array_equal(first[1], second[1])
        np.testing.assert_array_equal(first[2], second[2])

    def test_maximum_steps_stop_a_non_terminal_policy(self):
        environment = FrozenLake()
        q_table = np.zeros((16, 4))
        result = follow_greedy_policy(environment, q_table, max_steps=5)
        self.assertFalse(result["reached_goal"])
        self.assertEqual(len(result["route"]), 6)

    def test_invalid_training_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_parameters(0, 60, 10, 0.2, 0.9, 1.0, 0.03, 0.99)


if __name__ == "__main__":
    unittest.main()
