import pygame
import random
import sys
from game_art import draw_tetris_block

# --- Константы ---
BLOCK_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
SIDE_PANEL = 200
SCREEN_WIDTH = WIDTH + SIDE_PANEL
SCREEN_HEIGHT = HEIGHT

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (128, 128, 128)

COLORS = [
    (0, 255, 255),   # I - циан
    (255, 255, 0),   # O - жёлтый
    (160, 0, 240),   # T - фиолетовый
    (0, 255, 0),     # S - зелёный
    (255, 0, 0),     # Z - красный
    (0, 0, 255),     # J - синий
    (255, 165, 0),   # L - оранжевый
]

# Фигуры (каждая клетка задаётся смещениями от центра)
SHAPES = [
    [[1, 1, 1, 1]],                          # I
    [[1, 1],
     [1, 1]],                                # O
    [[0, 1, 0],
     [1, 1, 1]],                             # T
    [[0, 1, 1],
     [1, 1, 0]],                             # S
    [[1, 1, 0],
     [0, 1, 1]],                             # Z
    [[1, 0, 0],
     [1, 1, 1]],                             # J
    [[0, 0, 1],
     [1, 1, 1]],                             # L
]


class Piece:
    def __init__(self, shape_index):
        self.shape_index = shape_index
        self.shape = [row[:] for row in SHAPES[shape_index]]
        self.color = COLORS[shape_index]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        """Поворот по часовой стрелке."""
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        return rotated


class Tetris:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current = Piece(random.randint(0, len(SHAPES) - 1))
        self.next_piece = Piece(random.randint(0, len(SHAPES) - 1))
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500  # мс

    def valid_position(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    gx, gy = offset_x + x, offset_y + y
                    if gx < 0 or gx >= COLS or gy >= ROWS:
                        return False
                    if gy >= 0 and self.grid[gy][gx] is not None:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell:
                    gx = self.current.x + x
                    gy = self.current.y + y
                    if 0 <= gy < ROWS and 0 <= gx < COLS:
                        self.grid[gy][gx] = self.current.color
        self.clear_lines()
        self.spawn_new_piece()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = ROWS - len(new_grid)
        for _ in range(cleared):
            new_grid.insert(0, [None] * COLS)
        self.grid = new_grid

        if cleared > 0:
            self.lines += cleared
            self.score += [0, 100, 300, 500, 800][cleared] * self.level
            self.level = self.lines // 10 + 1
            self.fall_speed = max(100, 500 - (self.level - 1) * 40)

    def spawn_new_piece(self):
        self.current = self.next_piece
        self.next_piece = Piece(random.randint(0, len(SHAPES) - 1))
        if not self.valid_position(self.current.shape, self.current.x, self.current.y):
            self.game_over = True

    def move(self, dx, dy):
        if self.valid_position(self.current.shape,
                               self.current.x + dx,
                               self.current.y + dy):
            self.current.x += dx
            self.current.y += dy
            return True
        if dy > 0:
            self.lock_piece()
        return False

    def rotate_piece(self):
        rotated = self.current.rotate()
        # Простая стена-кик
        for dx in [0, -1, 1, -2, 2]:
            if self.valid_position(rotated, self.current.x + dx, self.current.y):
                self.current.shape = rotated
                self.current.x += dx
                return

    def hard_drop(self):
        while self.valid_position(self.current.shape,
                                  self.current.x,
                                  self.current.y + 1):
            self.current.y += 1
            self.score += 2
        self.lock_piece()

    def update(self, dt):
        if self.game_over:
            return
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            self.move(0, 1)


def draw_block(surface, x, y, color, size=BLOCK_SIZE):
    draw_tetris_block(surface, x, y, color, size)


def draw_grid_lines(surface):
    for x in range(COLS + 1):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0),
                         (x * BLOCK_SIZE, HEIGHT))
    for y in range(ROWS + 1):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE),
                         (WIDTH, y * BLOCK_SIZE))


def draw_next_piece(surface, piece, offset_x, offset_y):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                draw_block(surface,
                           offset_x + x * BLOCK_SIZE,
                           offset_y + y * BLOCK_SIZE,
                           piece.color)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Тетрис")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22, bold=True)
    big_font = pygame.font.SysFont("consolas", 40, bold=True)

    game = Tetris()

    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                else:
                    if event.key == pygame.K_r:
                        game = Tetris()

        game.update(dt)

        # --- Отрисовка ---
        screen.fill(BLACK)

        # Игровое поле
        for y in range(ROWS):
            for x in range(COLS):
                if game.grid[y][x]:
                    draw_block(screen, x * BLOCK_SIZE, y * BLOCK_SIZE,
                               game.grid[y][x])

        # Текущая фигура
        if not game.game_over:
            for y, row in enumerate(game.current.shape):
                for x, cell in enumerate(row):
                    if cell:
                        gx = (game.current.x + x) * BLOCK_SIZE
                        gy = (game.current.y + y) * BLOCK_SIZE
                        draw_block(screen, gx, gy, game.current.color)

        draw_grid_lines(screen)

        # Боковая панель
        panel_x = WIDTH + 20
        score_surf = font.render(f"Счёт: {game.score}", True, WHITE)
        level_surf = font.render(f"Уровень: {game.level}", True, WHITE)
        lines_surf = font.render(f"Линии: {game.lines}", True, WHITE)
        next_surf = font.render("Следующая:", True, WHITE)

        screen.blit(score_surf, (panel_x, 20))
        screen.blit(level_surf, (panel_x, 50))
        screen.blit(lines_surf, (panel_x, 80))
        screen.blit(next_surf, (panel_x, 130))

        draw_next_piece(screen, game.next_piece, panel_x + 20, 170)

        # Управление
        controls = [
            "← → движение",
            "↑ поворот",
            "↓ ускорить",
            "Пробел - сброс",
            "ESC - выход",
        ]
        for i, text in enumerate(controls):
            s = font.render(text, True, LIGHT_GRAY)
            screen.blit(s, (panel_x, HEIGHT - 150 + i * 28))

        # Game Over
        if game.game_over:
            over = big_font.render("GAME OVER", True, (255, 50, 50))
            restart = font.render("Нажмите R", True, WHITE)
            screen.blit(over, (WIDTH // 2 - over.get_width() // 2,
                               HEIGHT // 2 - 40))
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2,
                                  HEIGHT // 2 + 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()