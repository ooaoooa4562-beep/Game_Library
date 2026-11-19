import pygame
import random
import sys

pygame.init()

WIDTH = HEIGHT = 600
CELL = 20
COLS = ROWS = WIDTH // CELL

BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 30, 30)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)


def random_food(snake):
    while True:
        pos = (random.randrange(COLS), random.randrange(ROWS))
        if pos not in snake:
            return pos


def draw_cell(x, y, color):
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))


def game_over(score):
    screen.fill(BLACK)
    text = font.render(f"GAME OVER  Счёт: {score}", True, RED)
    hint = font.render("R — рестарт, ESC — выход", True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()


def main():
    snake = [(COLS // 2, ROWS // 2),
             (COLS // 2 - 1, ROWS // 2),
             (COLS // 2 - 2, ROWS // 2)]
    direction = (1, 0)
    food = random_food(snake)
    score = 0
    speed = 10

    while True:
        clock.tick(speed)

        # --- Управление WASD ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_s and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_a and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_d and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        # --- Движение ---
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Телепорт через стены
        new_head = (new_head[0] % COLS, new_head[1] % ROWS)

        # Столкновение с собой
        if new_head in snake and new_head != food:
            if game_over(score):
                return main()
            return

        snake.insert(0, new_head)

        # --- Еда ---
        if new_head == food:
            score += 10
            food = random_food(snake)
            # хвост НЕ убираем → змейка растёт
        else:
            snake.pop()

        # --- Отрисовка ---
        screen.fill(BLACK)
        draw_cell(food[0], food[1], RED)
        for i, (x, y) in enumerate(snake):
            draw_cell(x, y, GREEN if i == 0 else DARK_GREEN)

        text = font.render(f"Счёт: {score}  Длина: {len(snake)}", True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()


if __name__ == "__main__":
    main()