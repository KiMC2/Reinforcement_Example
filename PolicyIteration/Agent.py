import Environment

class Agent():
    def __init__(self, env):
        self.env = env
        self.value_func = [[0.0] * env.grid_x for _ in range(env.grid_y)]
        self.policy = [[0.0, 0.0, 0.0, 0.0] * env.grid_x for _ in range(env.grid_y)]
        self.discount_factor = 0.9

    def policy_evaluation(self):
        next_value = self.value_func

        for y in range(self.env.grid_y):
            for x in range(self.env.grid_x):
                value = 0.0

                state = (x, y)
                goal = (self.env.goal_x, self.env.goal_y)

                for action_index, action \
                        in enumerate(self.env.possible_actions):

                    # Goal(2, 2)
                    if state == goal:
                        value = 0.0
                        break

                    # 벨만 방정식
                    else:
                        next_state = self.env.step(state, action)
                        reward     = self.env.get_reward(next_state)
                        next_value = self.value_func[y][x]
                        value     += self.policy[y][x][action_index] * \
                                     (reward + self.discount_factor * next_value)

                self.value[y][x] = round(value, 2)

    def policy_improvement(self):
        next_policy = self.policy

        for y in range(self.env.grid_y):
            for x in range(self.env.grid_x):

                state = (x, y)
                goal = (self.env.goal_x, self.env.goal_y)

                if state == goal:
                    continue
                else:
                    max_value = -9999
                    max_index = []

                    for index, action in enumerate(self.env.possible_actions):
                        next_state = self.env.step(state, action)
                        reward     = self.env.get_reward(next_state)
                        next_value = self.value_func[y][x]
                        value       = reward + self.discount_factor * next_value

                        if value == max_value:
                            max_index.append(index)
                        elif value > max_value:
                            max_value = value
                            max_index.clear()
                            max_index.append(index)

                    # 행동 확률
                    

        self.policy = next_policy





if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)