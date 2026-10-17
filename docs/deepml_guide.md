# Deep-ML project guide

The induction sheet asks for a separate project on [Deep-ML](https://www.deep-ml.com/): **Q-Learning on Frozen-Lake from Scratch**. The local PS3 program is a study aid. It is not proof that the website project or its tests are complete.

## Where to go

1. Open [Deep-ML Projects](https://www.deep-ml.com/projects/q-learning-on-frozenlake-from-scratch/step/q-learning-on-frozenlake-from-scratch-0009).
2. Sign in if the site asks you to.
3. Open the project called **Q-Learning on FrozenLake from Scratch**.
4. Work through its steps in order, run the site's checks, and save a screenshot only after the site shows completion and passing results.

The public project page lists 16 steps in five parts:

1. **Q-table setup:** `init_q_table`, `max_q_value`, `greedy_action`.
2. **Epsilon-greedy action selection:** `sample_random_action`, `should_explore`, `epsilon_greedy_action`, `decay_epsilon`.
3. **Q-learning update rule:** `td_target`, `td_error`, `q_learning_update`.
4. **Training loop:** `interaction_step`, `run_training_episode`, `train_q_learning`.
5. **Policy and evaluation:** `extract_greedy_policy`, `run_greedy_episode`, `evaluate_success_rate`.

The page needs JavaScript for the full task instructions and tests. The publicly readable page shows the project outline, but the complete per-step directions and checks could not be read here. Use the platform's own instructions for function inputs, outputs, and rules. Do not copy assumptions from the local demo into the external project without checking them.

## Ideas to understand before starting

- A Q-table stores one value for each state and action.
- A greedy action chooses a largest Q-value. Epsilon-greedy sometimes chooses a random action to explore.
- The temporal-difference target is the reward plus the discounted best next-state value, except at a terminal state where there is no future value.
- The TD error is target minus the current Q-value. The learning rate controls how much the Q-value changes.
- Training lets the agent explore. Evaluation should use the learned greedy policy and report how often it reaches the goal.

## What to submit

Complete all steps and the site's checks yourself. Capture the requested screenshot showing the project and successful tests. This package has no Deep-ML completion screenshot and does not claim that the platform tests passed.
