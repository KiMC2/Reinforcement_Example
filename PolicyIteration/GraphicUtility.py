import pygame as pg
import sys

class GraphicUtility():
    def __init__(self, title, agent, env):
        self.agent = agent
        self.env = env

        # 한 칸의 pixel 크기
        self.grid_pixel = 100

        # 스크린 크기는 grid 칸 수에 의해 결정된다
        self.screen_size = env.grid_size * self.grid_pixel
        self.screen_color = (255, 255, 255)
        self.line_color = (0, 0, 0)

        # Screen 초기화
        pg.init()
        self.screen = pg.display.set_mode((self.screen_size , self.screen_size), 0, 32)
        pg.display.set_caption(title)

        # 이미지 (유닛, 장애물, 목표지점)
        self.img_padding = 0.5
        img_size = int(self.grid_pixel * (1.0 - self.img_padding))

        unit_img = pg.image.load('../img/rectangle.png')
        obstacle_img = pg.image.load('../img/triangle.png')
        goal_img = pg.image.load('../img/circle.png')

        self.unit = pg.transform.scale(unit_img, (img_size, img_size))
        self.obstacle = pg.transform.scale(obstacle_img, (img_size, img_size))
        self.goal = pg.transform.scale(goal_img, (img_size, img_size))


    def _check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    self.agent.policy_evaluation()
                elif event.key == pg.K_i:
                    self.agent.policy_improvement()
                elif event.key == pg.K_m:
                    self.agent.move()
                elif event.key == pg.K_r:
                    self.agent.reset()

    def _draw(self):

        # 배경화면 그리기
        pg.draw.rect(self.screen, self.screen_color, pg.Rect(0,0, self.screen_size, self.screen_size))

        # 라인 그리기
        for n in range(self.env.grid_size):
            # 왼쪽 선 그리기 |
            pg.draw.line(self.screen, self.line_color,
                         (0, n * self.grid_pixel), (self.screen_size, n * self.grid_pixel))
            pg.draw.line(self.screen, self.line_color,
                         (n * self.grid_pixel, 0), (n * self.grid_pixel, self.screen_size))  # 위쪽 선 그리기 ㅡ

        # 유닛, 장애물, 목표 그리기
        self._draw_img(self.unit, self.env.unit_coord)
        self._draw_img(self.goal, self.env.goal_coord)

        for coord in self.env.obstacle_coord:
            self._draw_img(self.obstacle, coord)

        # 텍스트 그리기
        for y in range(self.env.grid_size):
            for x in range(self.env.grid_size):
                self._draw_text(str(self.agent.value_func[y][x]), x, y)

        pg.display.flip()

    def _draw_img(self, image, coord):
        # 좌표 지점과 padding(0.4)을 더하고 곱하면 이미지 좌표
        x = (coord[0] + (self.img_padding / 2)) * self.grid_pixel
        y = (coord[1] + (self.img_padding / 2)) * self.grid_pixel

        self.screen.blit(image, (x, y))

    def _draw_text(self, text, x, y):
        font_size = int(self.grid_pixel * 0.1)
        font = pg.font.SysFont('Comic Sans MS', font_size)
        text = font.render(text, False, (0,0,0))

        font_pos = int(self.grid_pixel * 0.8)
        draw_x = x * self.grid_pixel + font_pos
        draw_y = y * self.grid_pixel + font_pos

        self.screen.blit(text, (draw_x, draw_y))

    def main_loop(self):
        while True:
            self._check_event()
            self._draw()
