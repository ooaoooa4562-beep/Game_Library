import pygame
from game_art import draw_snake_segment
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
    occupied=set(snake)
    free=[(x,y) for x in range(COLS) for y in range(ROWS) if (x,y) not in occupied]
    return random.choice(free) if free else None


def draw_cell(x, y, color, head=False, direction=(1, 0)):
    draw_snake_segment(screen, (x * CELL, y * CELL, CELL, CELL), head, direction)


def game_over(score):
    screen.fill(BLACK)
    text = font.render(f"GAME OVER  Счёт: {score}", True, RED)
    hint = font.render("R — рестарт, ESC — выход", True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    pygame.display.flip()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()


def round_game():
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
        if new_head in (snake if new_head == food else snake[:-1]):
            return game_over(score)

        snake.insert(0, new_head)

        # --- Еда ---
        if new_head == food:
            score += 10
            food = random_food(snake)
            if food is None: return game_over(score)
            speed=min(22,10+score//50)
            # хвост НЕ убираем → змейка растёт
        else:
            snake.pop()

        # --- Отрисовка ---
        screen.fill(BLACK)
        pygame.draw.circle(screen, (90, 20, 20), (food[0]*CELL+CELL//2+2, food[1]*CELL+CELL//2+2), CELL//3)
        pygame.draw.circle(screen, (245, 65, 75), (food[0]*CELL+CELL//2, food[1]*CELL+CELL//2), CELL//3)
        pygame.draw.circle(screen, (255, 190, 190), (food[0]*CELL+CELL//2-3, food[1]*CELL+CELL//2-3), 3)
        for i, (x, y) in enumerate(snake):
            draw_cell(x, y, GREEN if i == 0 else DARK_GREEN, i == 0, direction)

        text = font.render(f"Счёт: {score}  Длина: {len(snake)}", True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()


if __name__ == "__main__":
    while round_game():
        pass