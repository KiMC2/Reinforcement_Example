import pygame as pg
import sys

class GraphicUtility():
    def __init__(self, title, agent, grid_pixel=150, img_rate=0.5):
        self.agent = agent

        # 한 칸의 pixel 크기
        self.grid_pixel = grid_pixel

        # 스크린 크기는 grid 칸 수에 의해 결정된다
        self.screen_size = self.agent.env.grid_size * self.grid_pixel
        self.screen_color = (255, 255, 255)
        self.line_color = (0, 0, 0)

        # Screen 초기화
        pg.init()
        self.screen = pg.display.set_mode((self.screen_size , self.screen_size), 0, 32)
        pg.display.set_caption(title)

        # 이미지 (유닛, 장애물, 목표지점)
        self.img_padding = img_rate
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
        for n in range(self.agent.env.grid_size):
            # 왼쪽 선 그리기 |
            pg.draw.line(self.screen, self.line_color,
                         (0, n * self.grid_pixel), (self.screen_size, n * self.grid_pixel))
            pg.draw.line(self.screen, self.line_color,
                         (n * self.grid_pixel, 0), (n * self.grid_pixel, self.screen_size))  # 위쪽 선 그리기 ㅡ

        # 유닛, 장애물, 목표 그리기
        for coord in self.agent.env.obstacle_coord:
            self._draw_img(self.obstacle, coord)

        self._draw_img(self.goal, self.agent.env.goal_coord)
        self._draw_img(self.unit, self.agent.env.unit_coord)

        # 가치함수, 정책 (텍스트) 그리기
        for y in range(self.agent.env.grid_size):
            for x in range(self.agent.env.grid_size):
                self._draw_value_func(self.agent.value_func[y][x], x, y)
                self._draw_policy(self.agent.policy[y][x], x, y)


        pg.display.flip()

    def _draw_img(self, image, coord):
        # 좌표 지점과 padding(0.4)을 더하고 곱하면 이미지 좌표
        x = (coord[0] + (self.img_padding / 2)) * self.grid_pixel
        y = (coord[1] + (self.img_padding / 2)) * self.grid_pixel

        self.screen.blit(image, (x, y))

    def _draw_value_func(self, value_func, x, y):
        text = str(value_func)                              # 문자로 변환
        font_size = int(self.grid_pixel * 0.11)             # 칸의 크기에 맞게 문자 변환
        font = pg.font.SysFont('Helvetica', font_size)      # 폰트 설정
        text_img = font.render(text, False, (0,0,0))        # 이미지로 변환
        width, height = font.size(text)                     # 이미지 크기

        draw_x = x * self.grid_pixel + self.grid_pixel / 2 - width / 2
        draw_y = y * self.grid_pixel + self.grid_pixel / 2 - height / 2

        self.screen.blit(text_img, (draw_x, draw_y))

    def _draw_policy(self, policy, x, y):
        for action in self.agent.env.possible_actions:
            text = str(policy[action])
            font_size = int(self.grid_pixel * 0.11)
            font = pg.font.SysFont('Helvetica', font_size)
            text_img = font.render(text, False, (0, 0, 0))
            width, height = font.size(text)

            # 칸에서 텍스트 위치
            text_pos_x = 0
            text_pos_y = 0

            # 상
            if action == 0:
                text_pos_x = self.grid_pixel / 2 - width / 2
            elif action == 1:
                text_pos_x = self.grid_pixel / 2 - width / 2
                text_pos_y = self.grid_pixel - height
            elif action == 2:
                text_pos_y = self.grid_pixel / 2 - height / 2
            elif action == 3:
                text_pos_x = self.grid_pixel - width
                text_pos_y = self.grid_pixel / 2 - height / 2

            draw_x = x * self.grid_pixel + text_pos_x
            draw_y = y * self.grid_pixel + text_pos_y

            if not text == "0.0":
                self.screen.blit(text_img, (draw_x, draw_y))

    def main_loop(self):
        while True:
            self._check_event()
            self._draw()

