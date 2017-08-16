class Environment():
    def __init__(self):
        # 그리드 크기
        self.grid_size  = 5

        # 유닛 초기 지점 좌표
        self.unit_coord = (0, 0)

        # 목표지점 좌표
        self.goal_coord = (2, 2)

        # 장애물 좌표
        self.obstacle_coord = [[1, 2], [2, 1]]

        # 보상 테이블
        self.reward_table = [ [0] * self.grid_size for _ in range(self.grid_size) ]
        self.reward_table[self.goal_coord[0]][self.goal_coord[1]] = 1

        for o_coord in self.obstacle_coord:
            x, y = o_coord
            self.reward_table[y][x] = -1


        # 가능한 행동 모음( 상 하 좌 우 )
        self.possible_actions = [0, 1, 2, 3]

        # 상태 전이 확률률
        self.transition_probability = 1

    def step(self, state, action):
        x, y = state

        # 상
        if action == 0:
            y -= 1
            if y < 0:
                y += 1

        # 하
        elif action == 1:
            y += 1
            if y == self.grid_size:
                y -= 1

        # 좌
        elif action == 2:
            x -= 1
            if x < 0:
                x += 1

        # 우
        elif action == 3:
            x += 1
            if x == self.grid_size:
                x -= 1

        next_state = x, y
        return next_state

    def get_reward(self, state):
        x, y = state
        return self.reward_table[y][x]




