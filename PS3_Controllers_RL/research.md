# PS3 - Controllers and Reinforcement Learning

## Gate 1 - Feedback and error

### 1. What are a reference, measured value, feedback, and error?

The **reference** or **setpoint** is the value we want. The **measured value** is what a sensor or estimate says is happening now. **Feedback** sends that measured result back to the controller. With one common sign choice, **error** is `reference - measured value`.

### 2. Why is feedback better than blindly following a command?

Real systems can be pushed by wind, slopes, uneven ground, or changing loads. A controller that checks the result can adjust its next command. A pre-planned command does not correct itself when the result changes. Feedback still depends on good measurements and good controller settings.

## Gate 2 - Proportional control

### 3. What is proportional control?

The rule is `u = Kp * e`. `e` is the current error. `Kp` is the proportional gain. `u` is the command sent to the system, such as a steering or motor command. The sign of the error and gain must match the system's direction.

### 4. What happens when Kp changes?

Raising `Kp` usually makes the correction stronger and faster. If it is too high, the system can overshoot, swing back and forth, or become unstable. Lowering it usually makes the response slower and gentler.

### 5. Why can a P controller have steady-state error?

A P controller needs some error to create a command. If a constant disturbance needs a constant command, a small lasting error may be needed to produce it. The system and its limits also affect the final error.

## Gate 3 - PID control

### 6. What is PID control?

The rule is `u = Kp * e + Ki * integral(e) + Kd * derivative(e)`. The command uses the current error, the total error over time, and how quickly the error is changing. In a computer, the integral and derivative are estimated at each time step.

### 7. What do P, I, and D do?

- **P (proportional):** reacts to the current error. If a vehicle is far from the lane centre, P asks for a larger correction.
- **I (integral):** adds up error over time. It can reduce a small lasting offset, but can grow too large if the steering is held at its limit.
- **D (derivative):** reacts to how fast error is changing. It can reduce overshoot, but noise in the measurement can make it jumpy.

## Gate 4 - Path tracking

### 8. What is cross-track error?

Cross-track error is the side-to-side distance between the vehicle and the chosen path. It is often measured at a right angle to the path.

### 9. What is heading error?

Heading error is the angle between the way the vehicle is pointing and the direction of the path nearby.

### 10. Why use both errors?

A vehicle can be on the centre of a lane but pointing away from it. It can also point along the lane while being too far to one side. Position and heading errors together give more information for a smooth steering correction.

## Gate 5 - Reinforcement learning

### 11. What are an agent, environment, state, action, reward, and policy?

The **agent** chooses what to do. The **environment** is the place it acts in. The **state** describes its current situation. An **action** is a choice, such as moving left. A **reward** is a score after an action. A **policy** is a rule for choosing actions in different states.

### 12. What does Q(s, a) mean?

`Q(s, a)` is the agent's estimate of the future reward from taking action `a` in state `s`, then continuing to follow its policy. It helps the agent compare actions in the same state. It is an estimate learned from experience, not a promise of a result.

## Q-learning update used in the local example

`Q(s, a) = Q(s, a) + alpha * [reward + gamma * max(Q(next_state, next_action)) - Q(s, a)]`

`alpha` is the learning rate, which controls how much a new result changes the old value. `gamma` is the discount factor, which controls how much later rewards matter. At a terminal state, such as a hole or the goal, the local code uses no future reward. The Q-table starts at zero and is learned during training.

## References

- MathWorks, [What Is PID Control?](https://www.mathworks.com/discovery/pid-control.html).
- Hugging Face, [Introduction to Q-Learning](https://huggingface.co/learn/deep-rl-course/unit2/introduction).
- Hugging Face, [Hands-on Q-Learning with FrozenLake](https://huggingface.co/learn/deep-rl-course/unit2/hands-on).
