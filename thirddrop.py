import pygame
import random
import sys
import math

pygame.init()

# ============ НАСТРОЙКИ ============
TILE_SIZE = 80
COLS, ROWS = 8, 8
BOARD_X, BOARD_Y = 60, 120
WIDTH = BOARD_X * 2 + COLS * TILE_SIZE
HEIGHT = BOARD_Y + ROWS * TILE_SIZE + 80

FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Три в ряд - 5 уровней")
clock = pygame.time.Clock()

# Шрифты
font_big = pygame.font.SysFont("arial", 32, bold=True)
font_mid = pygame.font.SysFont("arial", 22, bold=True)
font_small = pygame.font.SysFont("arial", 18)

# Цвета
BG_TOP = (40, 20, 80)
BG_BOT = (20, 10, 40)
BOARD_BG = (30, 25, 60)
BOARD_LINE = (60, 50, 110)
WHITE = (255, 255, 255)
GOLD = (255, 210, 60)
TEXT_DARK = (30, 20, 50)

# Типы камней — цвета и отрисовка
# 0: рубин (красный), 1: изумруд (зелёный), 2: сапфир (синий),
# 3: топаз (жёлтый), 4: аметист (фиолетовый), 5: алмаз (голубой)
STONE_COLORS = [
    (220, 50, 70),    # рубин
    (50, 200, 90),    # изумруд
    (60, 120, 240),   # сапфир
    (250, 200, 50),   # топаз
    (170, 70, 220),   # аметист
    (70, 210, 230),   # алмаз
]

STONE_NAMES = ["Рубин", "Изумруд", "Сапфир", "Топаз", "Аметист", "Алмаз"]


def lighten(c, amt):
    return tuple(min(255, int(v + (255 - v) * amt)) for v in c)

def darken(c, amt):
    return tuple(max(0, int(v * (1 - amt))) for v in c)

def draw_gem(surface, kind, cx, cy, size):
    """Рисует красивый камень-иконку."""
    c = STONE_COLORS[kind]
    light = lighten(c, 0.55)
    dark = darken(c, 0.45)
    shine = lighten(c, 0.85)

    # Тень под камнем
    shadow = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 90),
                        (4, size - size // 4, size - 8, size // 4))
    surface.blit(shadow, (cx - size // 2, cy - size // 2))

    r = size // 2 - 4

    # Формы в зависимости от типа
    if kind == 0:  # рубин — огранённый ромб
        pts = [(cx, cy - r), (cx + r * 0.8, cy - r * 0.3),
               (cx + r * 0.6, cy + r * 0.7), (cx, cy + r),
               (cx - r * 0.6, cy + r * 0.7), (cx - r * 0.8, cy - r * 0.3)]
        pygame.draw.polygon(surface, dark, pts)
        inner = [(cx, cy - r + 4), (cx + r * 0.6, cy - r * 0.2),
                 (cx + r * 0.45, cy + r * 0.55), (cx, cy + r - 4),
                 (cx - r * 0.45, cy + r * 0.55), (cx - r * 0.6, cy - r * 0.2)]
        pygame.draw.polygon(surface, c, inner)
        pygame.draw.polygon(surface, light,
                            [(cx, cy - r + 10), (cx + r * 0.3, cy - r * 0.1),
                             (cx, cy + r * 0.2), (cx - r * 0.3, cy - r * 0.1)])
        pygame.draw.polygon(surface, shine,
                            [(cx - 4, cy - r + 16), (cx + 4, cy - r + 16),
                             (cx, cy - r + 30)])

    elif kind == 1:  # изумруд — шестиугольник
        pts = [(cx + r * math.cos(math.pi / 3 * i + math.pi / 6),
                cy + r * math.sin(math.pi / 3 * i + math.pi / 6)) for i in range(6)]
        pygame.draw.polygon(surface, dark, pts)
        inner = [(cx + (r - 5) * math.cos(math.pi / 3 * i + math.pi / 6),
                  cy + (r - 5) * math.sin(math.pi / 3 * i + math.pi / 6)) for i in range(6)]
        pygame.draw.polygon(surface, c, inner)
        # Грани
        for i in range(6):
            a1 = math.pi / 3 * i + math.pi / 6
            a2 = math.pi / 3 * (i + 1) + math.pi / 6
            pygame.draw.polygon(surface, light,
                                [(cx, cy),
                                 (cx + (r - 5) * math.cos(a1), cy + (r - 5) * math.sin(a1)),
                                 (cx + (r - 5) * math.cos(a2), cy + (r - 5) * math.sin(a2))])
        pygame.draw.circle(surface, shine, (cx - r // 4, cy - r // 3), 5)

    elif kind == 2:  # сапфир — круглый кабошон
        pygame.draw.circle(surface, dark, (cx, cy), r)
        pygame.draw.circle(surface, c, (cx, cy), r - 4)
        pygame.draw.circle(surface, light, (cx - r // 4, cy - r // 4), r // 2)
        pygame.draw.circle(surface, shine, (cx - r // 3, cy - r // 3), r // 5)

    elif kind == 3:  # топаз — квадрат с огранкой
        r2 = int(r * 0.85)
        pygame.draw.rect(surface, dark, (cx - r2, cy - r2, r2 * 2, r2 * 2), border_radius=6)
        pygame.draw.rect(surface, c, (cx - r2 + 4, cy - r2 + 4, r2 * 2 - 8, r2 * 2 - 8),
                         border_radius=6)
        pygame.draw.polygon(surface, light,
                            [(cx - r2 + 6, cy - r2 + 6), (cx + r2 // 2, cy - r2 + 6),
                             (cx - r2 + 6, cy + r2 // 2)])
        pygame.draw.line(surface, light, (cx - r2 + 8, cy + r2 - 8),
                         (cx + r2 - 8, cy - r2 + 8), 3)
        pygame.draw.circle(surface, shine, (cx - r2 // 2, cy - r2 // 2), 4)

    elif kind == 4:  # аметист — овал/капля
        pts = []
        for i in range(24):
            a = math.pi * 2 * i / 24
            rr = r * (0.75 + 0.25 * math.sin(a * 3))
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 1.05))
        pygame.draw.polygon(surface, dark, pts)
        inner = [(cx + (x - cx) * 0.82, cy + (y - cy) * 0.82) for x, y in pts]
        pygame.draw.polygon(surface, c, inner)
        pygame.draw.circle(surface, light, (cx - r // 3, cy - r // 3), r // 3)
        pygame.draw.circle(surface, shine, (cx - r // 3, cy - r // 3), r // 6)

    elif kind == 5:  # алмаз — бриллиант
        pts_top = [(cx - r, cy - r // 3), (cx - r // 2, cy - r),
                   (cx + r // 2, cy - r), (cx + r, cy - r // 3)]
        pts_bot = [(cx - r, cy - r // 3), (cx, cy + r),
                   (cx + r, cy - r // 3), (cx + r // 2, cy - r),
                   (cx - r // 2, cy - r)]
        pygame.draw.polygon(surface, dark, pts_bot)
        pygame.draw.polygon(surface, c, pts_top)
        # Грани
        pygame.draw.polygon(surface, light,
                            [(cx - r // 2, cy - r), (cx, cy - r // 3), (cx + r // 2, cy - r)])
        pygame.draw.polygon(surface, light,
                            [(cx - r // 2, cy - r), (cx - r, cy - r // 3), (cx, cy - r // 3)])
        pygame.draw.polygon(surface, shine,
                            [(cx, cy - r // 3), (cx + r, cy - r // 3), (cx, cy + r)])
        pygame.draw.polygon(surface, lighten(c, 0.9),
                            [(cx - r + 6, cy - r // 3 + 2), (cx - r // 2 + 4, cy - r + 3),
                             (cx - r // 2 + 6, cy - r // 3 - 2)])

    # Блик сверху
    hl = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(hl, (255, 255, 255, 70), (size // 2 - size // 6, size // 6),
                       max(3, size // 10))
    surface.blit(hl, (cx - size // 2, cy - size // 2))


class Level:
    def __init__(self, num, colors, moves, target, desc):
        self.num = num
        self.colors = colors      # сколько типов камней
        self.moves = moves
        self.target = target
        self.desc = desc


LEVELS = [
    Level(1, 4, 20, 800, "Соберите 800 очков"),
    Level(2, 5, 20, 1200, "Соберите 1200 очков"),
    Level(3, 5, 18, 1500, "Соберите 1500 очков"),
    Level(4, 6, 18, 1800, "Соберите 1800 очков"),
    Level(5, 6, 15, 2200, "Соберите 2200 очков"),
]


class Game:
    def __init__(self):
        self.level_index = 0
        self.score = 0
        self.total_score = 0
        self.state = "menu"  # menu, play, win, lose, gameover
        self.reset_level()

    def reset_level(self):
        lv = LEVELS[self.level_index]
        self.colors = lv.colors
        self.moves = lv.moves
        self.target = lv.target
        self.score = 0
        self.board = [[random.randint(0, self.colors - 1) for _ in range(COLS)]
                      for _ in range(ROWS)]
        self.selected = None
        self.anim = None
        self.falling = []
        self.flash = []
        self.msg = ""
        self.msg_timer = 0

        # Убираем изначальные совпадения
        while self.find_matches():
            for (r, c) in self.find_matches():
                self.board[r][c] = random.randint(0, self.colors - 1)
        self.state = "play"

    def find_matches(self):
        matched = set()
        for r in range(ROWS):
            run = 1
            for c in range(1, COLS):
                if self.board[r][c] == self.board[r][c - 1] != -1:
                    run += 1
                else:
                    if run >= 3:
                        for k in range(run):
                            matched.add((r, c - 1 - k))
                    run = 1
            if run >= 3:
                for k in range(run):
                    matched.add((r, COLS - 1 - k))
        for c in range(COLS):
            run = 1
            for r in range(1, ROWS):
                if self.board[r][c] == self.board[r - 1][c] != -1:
                    run += 1
                else:
                    if run >= 3:
                        for k in range(run):
                            matched.add((r - 1 - k, c))
                    run = 1
            if run >= 3:
                for k in range(run):
                    matched.add((ROWS - 1 - k, c))
        return matched

    def swap(self, a, b):
        self.board[a[0]][a[1]], self.board[b[0]][b[1]] = \
            self.board[b[0]][b[1]], self.board[a[0]][a[1]]

    def try_swap(self, a, b):
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
            return False
        self.swap(a, b)
        m = self.find_matches()
        if m:
            self.moves -= 1
            self.anim = {"type": "clear", "cells": m, "t": 0}
            self.selected = None
            return True
        else:
            self.swap(a, b)
            return False

    def process_matches(self):
        m = self.find_matches()
        if not m:
            return False
        gain = len(m) * 10 * (1 + (len(m) - 3) // 3 * 0.5)
        self.score += int(gain)
        for (r, c) in m:
            self.board[r][c] = -1
        self.flash = list(m)
        self.flash_timer = 0
        return True

    def collapse(self):
        for c in range(COLS):
            col_vals = [self.board[r][c] for r in range(ROWS) if self.board[r][c] != -1]
            new_col = [random.randint(0, self.colors - 1)
                       for _ in range(ROWS - len(col_vals))] + col_vals
            for r in range(ROWS):
                self.board[r][c] = new_col[r]

    def update(self):
        if self.state != "play":
            return
        if self.anim:
            self.anim["t"] += 1
            if self.anim["type"] == "clear" and self.anim["t"] >= 12:
                self.process_matches()
                self.collapse()
                self.anim = {"type": "fall", "t": 0}
            elif self.anim["type"] == "fall":
                if self.find_matches():
                    m = self.find_matches()
                    self.score += len(m) * 10
                    for (r, c) in m:
                        self.board[r][c] = -1
                    self.flash = list(m)
                    self.flash_timer = 0
                    self.collapse()
                    self.anim = {"type": "fall", "t": 0}
                else:
                    self.anim = None
                    # Проверка ходов
                    if self.moves <= 0 and self.score < self.target:
                        self.state = "lose"
                    elif self.score >= self.target:
                        self.state = "win"

    def click(self, pos):
        if self.state != "play" or self.anim:
            return
        bx, by = pos
        c = (bx - BOARD_X) // TILE_SIZE
        r = (by - BOARD_Y) // TILE_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS:
            if self.selected is None:
                self.selected = (r, c)
            elif self.selected == (r, c):
                self.selected = None
            else:
                if not self.try_swap(self.selected, (r, c)):
                    self.selected = (r, c)

    def draw(self, surf):
        # Фон
        for y in range(HEIGHT):
            t = y / HEIGHT
            col = (int(BG_TOP[0] * (1 - t) + BG_BOT[0] * t),
                   int(BG_TOP[1] * (1 - t) + BG_BOT[1] * t),
                   int(BG_TOP[2] * (1 - t) + BG_BOT[2] * t))
            pygame.draw.line(surf, col, (0, y), (WIDTH, y))

        if self.state == "menu":
            self.draw_menu(surf)
            return

        # Верхняя панель
        lv = LEVELS[self.level_index]
        title = font_big.render(f"Уровень {lv.num}", True, GOLD)
        surf.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        # Очки и ходы
        score_txt = font_mid.render(f"Очки: {self.score}/{self.target}", True, WHITE)
        surf.blit(score_txt, (BOARD_X, 55))
        moves_txt = font_mid.render(f"Ходы: {self.moves}", True, WHITE)
        surf.blit(moves_txt, (WIDTH - BOARD_X - moves_txt.get_width(), 55))

        # Прогресс-бар
        bar_x, bar_y = BOARD_X, 88
        bar_w = COLS * TILE_SIZE
        pygame.draw.rect(surf, (60, 50, 90), (bar_x, bar_y, bar_w, 16), border_radius=8)
        prog = min(1.0, self.score / self.target)
        pygame.draw.rect(surf, GOLD, (bar_x, bar_y, int(bar_w * prog), 16), border_radius=8)

        # Поле
        pygame.draw.rect(surf, BOARD_BG,
                         (BOARD_X - 6, BOARD_Y - 6,
                          COLS * TILE_SIZE + 12, ROWS * TILE_SIZE + 12),
                         border_radius=12)

        # Сетка
        for r in range(ROWS):
            for c in range(COLS):
                x = BOARD_X + c * TILE_SIZE
                y = BOARD_Y + r * TILE_SIZE
                cell_rect = pygame.Rect(x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4)
                # чередование клеток
                cc = (40, 35, 75) if (r + c) % 2 == 0 else (35, 30, 68)
                pygame.draw.rect(surf, cc, cell_rect, border_radius=6)

        # Подсветка выделения
        if self.selected:
            r, c = self.selected
            x = BOARD_X + c * TILE_SIZE
            y = BOARD_Y + r * TILE_SIZE
            pygame.draw.rect(surf, GOLD, (x + 1, y + 1, TILE_SIZE - 2, TILE_SIZE - 2),
                             3, border_radius=6)

        # Камни
        for r in range(ROWS):
            for c in range(COLS):
                k = self.board[r][c]
                if k == -1:
                    continue
                x = BOARD_X + c * TILE_SIZE + TILE_SIZE // 2
                y = BOARD_Y + r * TILE_SIZE + TILE_SIZE // 2
                if self.anim and self.anim["type"] == "clear":
                    t = self.anim["t"] / 12
                    size = int(TILE_SIZE * 0.85 * (1 - t * 0.5))
                    # Мерцание
                    alpha = 1 - t
                    # Отрисовать уменьшающийся
                    if (r, c) in self.anim["cells"]:
                        tmp = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        draw_gem(tmp, k, TILE_SIZE // 2, TILE_SIZE // 2, size)
                        tmp.set_alpha(int(255 * alpha))
                        surf.blit(tmp, (BOARD_X + c * TILE_SIZE, BOARD_Y + r * TILE_SIZE))
                        continue
                draw_gem(surf, k, x, y, int(TILE_SIZE * 0.85))

        # Сообщение о конце
        if self.state in ("win", "lose"):
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surf.blit(overlay, (0, 0))
            if self.state == "win":
                txt = font_big.render("Уровень пройден!", True, GOLD)
            else:
                txt = font_big.render("Ходы закончились", True, (255, 120, 120))
            surf.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 80))

            info = font_mid.render(f"Счёт: {self.score}  /  Цель: {self.target}",
                                   True, WHITE)
            surf.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 - 20))

            hint = font_small.render("Нажмите ПРОБЕЛ, чтобы продолжить", True, (200, 200, 220))
            surf.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 30))

        if self.state == "gameover":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            surf.blit(overlay, (0, 0))
            txt = font_big.render("Игра окончена", True, GOLD)
            surf.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 60))
            info = font_mid.render(f"Общий счёт: {self.total_score}", True, WHITE)
            surf.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2))
            hint = font_small.render("Нажмите ПРОБЕЛ для новой игры", True, (200, 200, 220))
            surf.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 40))

    def draw_menu(self, surf):
        title = font_big.render("ТРИ В РЯД", True, GOLD)
        surf.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))
        sub = font_mid.render("5 уровней драгоценных камней", True, WHITE)
        surf.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 110))

        # Примеры камней
        for i in range(6):
            x = WIDTH // 2 - 3 * 90 + i * 90
            draw_gem(surf, i, x, 200, 70)
            name = font_small.render(STONE_NAMES[i], True, (200, 200, 220))
            surf.blit(name, (x - name.get_width() // 2, 245))

        y0 = 310
        for i, lv in enumerate(LEVELS):
            line = font_small.render(
                f"Уровень {lv.num}: {lv.desc}, ходов: {lv.moves}", True,
                (220, 220, 240))
            surf.blit(line, (WIDTH // 2 - line.get_width() // 2, y0 + i * 28))

        hint = font_mid.render("Нажмите ПРОБЕЛ чтобы начать", True, GOLD)
        surf.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 60))


def main():
    game = Game()
    game.state = "menu"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.state == "play":
                    game.click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if game.state == "menu":
                        game.level_index = 0
                        game.total_score = 0
                        game.reset_level()
                    elif game.state == "win":
                        game.total_score += game.score
                        if game.level_index + 1 < len(LEVELS):
                            game.level_index += 1
                            game.reset_level()
                        else:
                            game.state = "gameover"
                    elif game.state == "lose":
                        game.reset_level()
                    elif game.state == "gameover":
                        game.state = "menu"

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()