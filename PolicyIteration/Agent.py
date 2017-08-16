class Agent():
    def __init__(self, env):
        # 환경
        self.env = env

        # 가치함수 테이블
        self.value_func = [[0.0] * env.grid_size for _ in range(env.grid_size)]

        # 정책 테이블
        self.policy = [[[0.25, 0.25, 0.25, 0.25]] * env.grid_size for _ in range(env.grid_size)]

        # 감가율
        self.discount_factor = 0.9

    def _get_policy(self, state, action):
        x, y = state
        return self.policy[y][x][action]

    def _get_value_func(self, state):
        x, y = state
        return self.value_func[y][x]

    def policy_evaluation(self):
        next_value_func = [[0.0] * self.env.grid_size for _ in range(self.env.grid_size)]

        for y in range(self.env.grid_size):
            for x in range(self.env.grid_size):
                value = 0.0

                # 현재 상태 및 목표
                state = (x, y)

                # 각 상태의 모든 행동에 대한 가치함수의 합을 구한다.
                for action in self.env.possible_actions:

                    # 목표 지점에서는 가치함수를 따지지 않는다.
                    if state == self.env.goal_coord:
                        value = 0.0
                        break

                    # 벨만 방정식
                    else:
                        # 다음 상태
                        next_state = self.env.step(state, action)

                        # 다음 상태의 보상
                        reward     = self.env.get_reward(next_state)

                        # 다음 상태의 가치함수
                        next_value = self._get_value_func(next_state)

                        # 가치 함수 = 정책 x (다음 상태의 보상 + 감가율 x 다음 상태 가치함수)
                        value     += self._get_policy(state, action) * \
                                     (reward + self.discount_factor * next_value)


                # 업데이트
                next_value_func[y][x] = round(value, 2)
        self.value_func = next_value_func

    def policy_improvement(self):
        # 갱신할 policy
        next_policy = self.policy

        for y in range(self.env.grid_size):
            for x in range(self.env.grid_size):

                state = (x, y)

                if state == self.env.goal_coord:
                    continue
                else:
                    # 최댓값
                    max_value = -9999
                    max_actions = []

                    for action in self.env.possible_actions:
                        next_state = self.env.step(state, action)
                        reward = self.env.get_reward(next_state)
                        next_value = self._get_value_func(next_state)

                        # 행동에 대한 가치함수
                        value = reward + self.discount_factor * next_value


                        # 최댓값과 같다면 저장만 더하기
                        if value == max_value:
                            max_actions.append(action)

                        # 최댓값보다 큰 값이면 새롭게 최댓값 저장
                        elif value > max_value:
                            max_value = value
                            max_actions.clear()
                            max_actions.append(action)

                    # 정책 저장
                    policy = [0.0, 0.0, 0.0, 0.0]
                    for action in max_actions:
                        policy[action] = 1 / len(max_actions)

                    self.policy[y][x] = policy

    def move(self):
        pass

    def reset(self):
        pass
