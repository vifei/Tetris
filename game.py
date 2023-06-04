import pygame
import random

# 初始化 Pygame
pygame.init()

# 游戏窗口的尺寸
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 游戏区域的尺寸
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
PLAY_TOP_LEFT_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
PLAY_TOP_LEFT_Y = WINDOW_HEIGHT - PLAY_HEIGHT

# 方块尺寸和颜色
BLOCK_SIZE = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(0, 0, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128), (255, 0, 255)]

# 右侧栏尺寸和颜色
SIDEBAR_WIDTH = 200
SIDEBAR_HEIGHT = PLAY_HEIGHT
SIDEBAR_TOP_LEFT_X = WINDOW_WIDTH - SIDEBAR_WIDTH
SIDEBAR_TOP_LEFT_Y = PLAY_TOP_LEFT_Y

# 右侧栏字体颜色和大小
FONT_COLOR = WHITE
FONT_SIZE = 24

# 初始化游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH + SIDEBAR_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("俄罗斯方块")


# 方块类
class Block:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def draw(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    rect = pygame.Rect(
                        self.x + col * BLOCK_SIZE, self.y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                    )
                    pygame.draw.rect(window, self.color, rect)
                    pygame.draw.rect(window, WHITE, rect, 1)


# 游戏区域类
class PlayArea:
    def __init__(self):
        self.grid = [[BLACK] * (PLAY_WIDTH // BLOCK_SIZE) for _ in range(PLAY_HEIGHT // BLOCK_SIZE)]

    def draw(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                rect = pygame.Rect(
                    PLAY_TOP_LEFT_X + col * BLOCK_SIZE,
                    PLAY_TOP_LEFT_Y + row * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(window, self.grid[row][col], rect)
                pygame.draw.rect(window, WHITE, rect, 1)

    def is_collision(self, block):
        for row in range(len(block.shape)):
            for col in range(len(block.shape[row])):
                if (
                        block.shape[row][col]
                        and (
                        col + block.x // BLOCK_SIZE - PLAY_TOP_LEFT_X // BLOCK_SIZE + 1 > len(self.grid[0])
                        or row + block.y // BLOCK_SIZE + 1 >= len(self.grid)
                        or self.grid[(row + block.y // BLOCK_SIZE + 1) % 20][
                            (col + block.x // BLOCK_SIZE - PLAY_TOP_LEFT_X // BLOCK_SIZE) % 10] != BLACK
                )
                ):
                    return True

        return False

    def can_moveleft(self, block):
        for row in range(len(block.shape)):
            for col in range(len(block.shape[row])):
                if (
                        block.shape[row][col]
                        and (
                        col + block.x // BLOCK_SIZE - PLAY_TOP_LEFT_X // BLOCK_SIZE <= 0
                        or self.grid[row + block.y // BLOCK_SIZE][
                            col + block.x // BLOCK_SIZE - PLAY_TOP_LEFT_X // BLOCK_SIZE - 1] != BLACK
                )
                ):
                    return False

        return True

    def can_moveright(self, block):
        for row in range(len(block.shape)):
            for col in range(len(block.shape[row])):
                if (
                        block.shape[row][col]
                        and (
                        col + block.x // BLOCK_SIZE - PLAY_TOP_LEFT_X // BLOCK_SIZE + 1 >= len(self.grid[0])
                        or self.grid[row + block.y // BLOCK_SIZE][
                            col + block.x // BLOCK_SIZE - PLAY_TOP_LEFT_X // BLOCK_SIZE + 1] != BLACK
                )
                ):
                    return False

        return True

    

    def add_block(self, block):
        for row in range(len(block.shape)):
            for col in range(len(block.shape[row])):
                if block.shape[row][col]:
                    grid_row = row + block.y // BLOCK_SIZE
                    grid_col = col + (block.x - PLAY_TOP_LEFT_X) // BLOCK_SIZE
                    print(grid_col)
                    if 0 <= grid_row < len(self.grid) and 0 <= grid_col < len(self.grid[0]):
                        self.grid[grid_row][grid_col] = block.color

    def remove_complete_rows(self, score):
        complete_rows = []
        for row in range(len(self.grid)):
            if all(cell != BLACK for cell in self.grid[row]):
                score += 10
                complete_rows.append(row)

        for row in complete_rows:
            del self.grid[row]
            self.grid.insert(0, [BLACK] * (PLAY_WIDTH // BLOCK_SIZE))

        return  score


# 俄罗斯方块类
class Tetris:
    def __init__(self):
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.play_area = PlayArea()
        self.score = 0
        self.last_fall_time = pygame.time.get_ticks()  # 记录上次方块下落的时间
        self.speed = 500

    def get_random_block(self):
        shape = random.choice(
            [
                [[1, 1, 1, 1]],
                [[1, 1], [1, 1]],
                [[1, 1, 0], [0, 1, 1]],
                [[0, 1, 1], [1, 1, 0]],
                [[1, 0, 0], [1, 1, 1]],
                [[0, 0, 1], [1, 1, 1]],
                [[1, 1, 1], [0, 1, 0]],
            ]
        )
        color = random.choice(COLORS[1:])

        # 调整初始位置
        x = PLAY_TOP_LEFT_X + BLOCK_SIZE * 3
        y = PLAY_TOP_LEFT_Y - BLOCK_SIZE  # 向上偏移一个方块的高度

        return Block(x, y, shape, color)

    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, WHITE)
        window.blit(text, (PLAY_TOP_LEFT_X + 20, WINDOW_HEIGHT // 2 - 50))

    def change_speed(self, score):
        speed_level = [(500, 0, 40), (400, 41, 100), (300, 101, 150), (200, 151, None)]
        for speed, score_start, score_stop in speed_level:
            if score_stop and score_start <= score <= score_stop:
                return speed
            elif score_stop is None and score >= score_start:
                return speed

    def update(self):
        current_time = pygame.time.get_ticks()
        self.speed = self.change_speed(self.score)
        if current_time - self.last_fall_time >= self.speed: 
            self.last_fall_time = current_time
            if not self.play_area.is_collision(self.current_block):
                self.current_block.y += BLOCK_SIZE

        if self.play_area.is_collision(self.current_block):
            self.play_area.add_block(self.current_block)
            self.score = self.play_area.remove_complete_rows(self.score)

            self.current_block = self.next_block
            self.next_block = self.get_random_block()

            if self.play_area.is_collision(self.current_block):
                self.game_over()
                return

        self.draw()

    def draw(self):
        window.fill(BLACK)

        self.play_area.draw()
        self.current_block.draw()

        self.draw_score()
        self.draw_next_block()

        pygame.draw.rect(window, WHITE, (PLAY_TOP_LEFT_X, PLAY_TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)
        pygame.draw.rect(window, WHITE, (SIDEBAR_TOP_LEFT_X, SIDEBAR_TOP_LEFT_Y, SIDEBAR_WIDTH, SIDEBAR_HEIGHT), 4)

        # 绘制网格线
        for x in range(PLAY_TOP_LEFT_X, PLAY_TOP_LEFT_X + PLAY_WIDTH, BLOCK_SIZE):
            pygame.draw.line(window, WHITE, (x, PLAY_TOP_LEFT_Y), (x, PLAY_TOP_LEFT_Y + PLAY_HEIGHT))
        for y in range(PLAY_TOP_LEFT_Y, PLAY_TOP_LEFT_Y + PLAY_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(window, WHITE, (PLAY_TOP_LEFT_X, y), (PLAY_TOP_LEFT_X + PLAY_WIDTH, y))

        pygame.display.update()

    def draw_score(self):
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render("Score: " + str(self.score), True, FONT_COLOR)
        window.blit(text, (SIDEBAR_TOP_LEFT_X + 20, SIDEBAR_TOP_LEFT_Y + 50))

    def draw_next_block(self):
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render("Next Block:", True, FONT_COLOR)
        window.blit(text, (SIDEBAR_TOP_LEFT_X + 20, SIDEBAR_TOP_LEFT_Y + 150))

        next_block_x = SIDEBAR_TOP_LEFT_X + 20
        next_block_y = SIDEBAR_TOP_LEFT_Y + 200
        next_block = self.next_block
        for row in range(len(next_block.shape)):
            for col in range(len(next_block.shape[row])):
                if next_block.shape[row][col]:
                    pygame.draw.rect(
                        window,
                        next_block.color,
                        (
                            next_block_x + col * BLOCK_SIZE,
                            next_block_y + row * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

    def game_over(self):
        self.draw()
        self.draw_game_over()
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()

    def move_left(self):
        if self.play_area.can_moveleft(self.current_block):
            self.current_block.x -= BLOCK_SIZE

        self.update()

    def move_right(self):
        if self.play_area.can_moveright(self.current_block):
            self.current_block.x += BLOCK_SIZE

        self.update()

    def move_down(self):
        if not self.play_area.is_collision(self.current_block):
            self.current_block.y += BLOCK_SIZE
        
        self.update()


    def rotate_block(self):
        old_block = self.current_block
        new_shape = list(zip(*reversed(old_block.shape)))  # 旋转方块的形状

        # 创建新的方块对象并设置旋转后的属性
        new_block = Block(old_block.x, old_block.y, new_shape, old_block.color)

        # 检查旋转后的方块是否与边界或已停止的方块发生碰撞
        if ( not self.play_area.is_collision(new_block) and 
            self.play_area.can_moveleft(new_block) and self.play_area.can_moveright(new_block) ):
            # 没有碰撞，更新为旋转后的方块
            self.current_block = new_block

        self.update()


# 游戏主循环
def main():
    clock = pygame.time.Clock()
    tetris = Tetris()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_left()
                elif event.key == pygame.K_RIGHT:
                    tetris.move_right()
                elif event.key == pygame.K_UP:
                    tetris.rotate_block()
                elif event.key == pygame.K_DOWN:
                    tetris.move_down()

        tetris.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
