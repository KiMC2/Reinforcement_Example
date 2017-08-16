import pygame as pg

class Environment():
    def __init__(self):
        self.grid_x     = 5
        self.grid_y     = 5
        self.grid_pixel = 100

        self.goal_x     = 2
        self.goal_y     = 2


        self.reward = [ [0.0] * self.grid_x for _ in range(self.grid_y) ]

        self.possible_action = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        self.transition_probability = 1

    def _boundary_check(self, x, y):
        return (x == 0 or x == self.grid_x - 1 or \
                y == 0 or y == self.grid_y - 1)

    def step(self, state, action):
        x, y = state

        if not self._boundary_check(x, y):
            if action == 'UP':      y -= 1
            elif action == 'DOWN':  y += 1
            elif action == 'LEFT':  x -= 1
            elif action == 'RIGHT': x += 1

        return x, y

    def get_reward(self, state, action):
        x, y = self.step(state, action)
        return self.reward[x][y]

if __name__ == '__main__':
    env = Environment()

