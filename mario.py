import pygame
import sys
from game_art import draw_mario, draw_goomba

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Platformer")
clock = pygame.time.Clock()

# Цвета
SKY = (107, 140, 255)
GROUND_COLOR = (139, 69, 19)
BRICK = (200, 80, 40)
GREEN = (0, 180, 0)
RED = (220, 30, 30)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
COIN_COLOR = (255, 215, 0)
FLAG_COLOR = (0, 200, 0)

# Безопасная инициализация шрифтов
try:
    FONT = pygame.font.SysFont("arial", 32, bold=True)
    SMALL_FONT = pygame.font.SysFont("arial", 22, bold=True)
    if FONT is None:
        raise Exception()
except Exception:
    FONT = pygame.font.Font(None, 36)
    SMALL_FONT = pygame.font.Font(None, 26)

GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_STRENGTH = -15


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 40)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1
        self.anim = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False

        self.vy += GRAVITY
        if self.vy > 18:
            self.vy = 18

        self.rect.x += self.vx
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.rect.right = p.rect.left
                elif self.vx < 0:
                    self.rect.left = p.rect.right

        self.rect.y += self.vy
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vy > 0:
                    self.rect.bottom = p.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.rect.bottom
                    self.vy = 0

        if self.vx != 0:
            self.anim += 1

    def draw(self, surf, cam_x):
        draw_mario(surf, x, y, self.facing, self.anim if self.vx else 0)


class Enemy:
    def __init__(self, x, y, left, right):
        self.rect = pygame.Rect(x, y, 30, 28)
        self.left = left
        self.right = right
        self.vx = -2
        self.alive = True
        self.squash_timer = 0

    def update(self, platforms):
        if not self.alive:
            if self.squash_timer > 0:
                self.squash_timer -= 1
            return
        self.rect.x += self.vx
        if self.rect.left < self.left:
            self.rect.left = self.left
            self.vx = 2
        if self.rect.right > self.right:
            self.rect.right = self.right
            self.vx = -2
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.rect.right = p.rect.left
                    self.vx = -2
                else:
                    self.rect.left = p.rect.right
                    self.vx = 2

    def draw(self, surf, cam_x):
        x = self.rect.x - cam_x
        y = self.rect.y
        if not self.alive:
            if self.squash_timer > 0:
                pygame.draw.rect(surf, BROWN, (x, y + 20, 30, 8))
            return
        draw_goomba(surf, self.rect.move(-cam_x, 0))


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False
        self.t = 0

    def update(self):
        self.t += 1

    def draw(self, surf, cam_x):
        if self.collected:
            return
        x = self.rect.x - cam_x
        y = self.rect.y
        w = abs(20 * (0.5 + 0.5 * (self.t % 40) / 40))
        if w < 4:
            w = 4
        pygame.draw.ellipse(surf, COIN_COLOR, (x + (20 - w) / 2, y, w, 20))
        pygame.draw.ellipse(surf, (200, 160, 0), (x + (20 - w) / 2, y, w, 20), 2)


class Platform:
    def __init__(self, x, y, w, h, kind="ground"):
        self.rect = pygame.Rect(x, y, w, h)
        self.kind = kind


class Level:
    def __init__(self, name):
        self.name = name
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.flag = None
        self.width = 0
        self.spawn = (100, 400)
        self.decor = []

    def draw_bg(self, surf, cam_x):
        surf.fill(SKY)
        for (cx, cy, size) in self.decor:
            px = cx - cam_x * 0.3
            px = px % (self.width + 400) - 200
            pygame.draw.ellipse(surf, WHITE, (px, cy, 80, 35))
            pygame.draw.ellipse(surf, WHITE, (px + 20, cy - 15, 60, 35))
            pygame.draw.ellipse(surf, WHITE, (px + 45, cy, 70, 35))

    def draw(self, surf, cam_x):
        self.draw_bg(surf, cam_x)
        for p in self.platforms:
            px = p.rect.x - cam_x
            if px + p.rect.w < -10 or px > WIDTH + 10:
                continue
            if p.kind == "ground":
                pygame.draw.rect(surf, GROUND_COLOR, (px, p.rect.y, p.rect.w, p.rect.h))
                pygame.draw.rect(surf, (100, 50, 10), (px, p.rect.y, p.rect.w, p.rect.h), 3)
                for gx in range(0, p.rect.w, 20):
                    pygame.draw.rect(surf, GREEN, (px + gx, p.rect.y, 4, 6))
            elif p.kind == "brick":
                pygame.draw.rect(surf, BRICK, (px, p.rect.y, p.rect.w, p.rect.h))
                for by in range(0, p.rect.h, 16):
                    for bx in range(0, p.rect.w, 20):
                        offset = 10 if (by // 16) % 2 == 1 else 0
                        pygame.draw.rect(surf, (120, 40, 20),
                                         (px + bx + offset, p.rect.y + by, 18, 14), 2)
            elif p.kind == "block":
                pygame.draw.rect(surf, (180, 100, 50), (px, p.rect.y, p.rect.w, p.rect.h))
                pygame.draw.rect(surf, (100, 60, 20), (px, p.rect.y, p.rect.w, p.rect.h), 3)
                pygame.draw.rect(surf, (240, 240, 240),
                                 (px + 4, p.rect.y + 4, p.rect.w - 8, p.rect.h - 8), 2)

        for c in self.coins:
            c.draw(surf, cam_x)
        for e in self.enemies:
            e.draw(surf, cam_x)

        if self.flag:
            fx = self.flag[0] - cam_x
            fy = self.flag[1]
            pygame.draw.rect(surf, BLACK, (fx, fy, 6, 100))
            pygame.draw.polygon(surf, FLAG_COLOR,
                                [(fx + 6, fy), (fx + 56, fy + 15), (fx + 6, fy + 30)])


def build_level1():
    lvl = Level("Уровень 1")
    lvl.width = 3200
    lvl.spawn = (80, 400)

    lvl.platforms.append(Platform(0, 520, 1200, 80, "ground"))
    lvl.platforms.append(Platform(1350, 520, 700, 80, "ground"))
    lvl.platforms.append(Platform(2150, 520, 1050, 80, "ground"))

    lvl.platforms.append(Platform(300, 400, 120, 30, "brick"))
    lvl.platforms.append(Platform(500, 300, 80, 30, "block"))
    lvl.platforms.append(Platform(650, 380, 120, 30, "brick"))
    lvl.platforms.append(Platform(850, 300, 80, 30, "block"))
    lvl.platforms.append(Platform(1000, 380, 160, 30, "brick"))
    lvl.platforms.append(Platform(1450, 400, 100, 30, "block"))
    lvl.platforms.append(Platform(1600, 320, 160, 30, "brick"))
    lvl.platforms.append(Platform(1800, 250, 80, 30, "block"))
    lvl.platforms.append(Platform(1950, 380, 120, 30, "brick"))
    lvl.platforms.append(Platform(2250, 400, 100, 30, "block"))
    lvl.platforms.append(Platform(2400, 300, 140, 30, "brick"))
    lvl.platforms.append(Platform(2600, 380, 120, 30, "block"))
    lvl.platforms.append(Platform(2800, 300, 80, 30, "brick"))

    for cx, cy in [
        (320, 360), (350, 360), (380, 360),
        (520, 260), (550, 260),
        (680, 340), (710, 340), (740, 340),
        (880, 260), (910, 260),
        (1200, 460), (1230, 460),
        (1480, 360), (1510, 360),
        (1640, 280), (1670, 280), (1700, 280),
        (1830, 210), (1860, 210),
        (1980, 340), (2010, 340),
        (2280, 360), (2310, 360),
        (2440, 260), (2470, 260), (2500, 260),
        (2640, 340), (2670, 340),
        (2840, 260), (2870, 260),
        (3000, 460), (3030, 460), (3060, 460)
    ]:
        lvl.coins.append(Coin(cx, cy))

    lvl.enemies.append(Enemy(450, 492, 350, 900))
    lvl.enemies.append(Enemy(1400, 492, 1350, 1600))
    lvl.enemies.append(Enemy(1700, 492, 1600, 2050))
    lvl.enemies.append(Enemy(2300, 492, 2150, 2700))
    lvl.enemies.append(Enemy(2900, 492, 2800, 3150))

    lvl.flag = (3100, 420)

    lvl.decor = [
        (200, 80, 1), (600, 120, 1), (1000, 60, 1),
        (1500, 100, 1), (2000, 70, 1), (2500, 110, 1), (2900, 80, 1)
    ]
    return lvl


def build_level2():
    lvl = Level("Уровень 2")
    lvl.width = 3600
    lvl.spawn = (80, 400)

    lvl.platforms.append(Platform(0, 520, 600, 80, "ground"))
    lvl.platforms.append(Platform(750, 520, 500, 80, "ground"))
    lvl.platforms.append(Platform(1450, 520, 400, 80, "ground"))
    lvl.platforms.append(Platform(2050, 520, 500, 80, "ground"))
    lvl.platforms.append(Platform(2750, 520, 850, 80, "ground"))

    lvl.platforms.append(Platform(620, 440, 100, 30, "block"))
    lvl.platforms.append(Platform(1260, 440, 160, 30, "brick"))
    lvl.platforms.append(Platform(1860, 440, 160, 30, "brick"))
    lvl.platforms.append(Platform(2560, 440, 160, 30, "brick"))

    lvl.platforms.append(Platform(200, 380, 100, 30, "brick"))
    lvl.platforms.append(Platform(400, 300, 100, 30, "block"))
    lvl.platforms.append(Platform(600, 240, 100, 30, "brick"))
    lvl.platforms.append(Platform(900, 340, 120, 30, "block"))
    lvl.platforms.append(Platform(1100, 260, 100, 30, "brick"))
    lvl.platforms.append(Platform(1500, 380, 120, 30, "block"))
    lvl.platforms.append(Platform(1700, 300, 100, 30, "brick"))
    lvl.platforms.append(Platform(2100, 340, 120, 30, "block"))
    lvl.platforms.append(Platform(2300, 260, 100, 30, "brick"))
    lvl.platforms.append(Platform(2500, 360, 100, 30, "block"))
    lvl.platforms.append(Platform(2800, 300, 120, 30, "brick"))
    lvl.platforms.append(Platform(3000, 380, 100, 30, "block"))
    lvl.platforms.append(Platform(3200, 300, 120, 30, "brick"))

    for cx, cy in [
        (220, 340), (250, 340), (280, 340),
        (420, 260), (450, 260),
        (620, 200), (650, 200),
        (920, 300), (950, 300),
        (1120, 220), (1150, 220),
        (1280, 400), (1310, 400), (1340, 400),
        (1520, 340), (1550, 340),
        (1720, 260), (1750, 260),
        (1880, 400), (1910, 400),
        (2120, 300), (2150, 300),
        (2320, 220), (2350, 220),
        (2520, 320), (2550, 320),
        (2820, 260), (2850, 260),
        (3020, 340), (3050, 340),
        (3220, 260), (3250, 260),
        (3400, 460), (3430, 460), (3460, 460)
    ]:
        lvl.coins.append(Coin(cx, cy))

    lvl.enemies.append(Enemy(250, 492, 100, 550))
    lvl.enemies.append(Enemy(800, 492, 760, 1200))
    lvl.enemies.append(Enemy(1500, 492, 1460, 1800))
    lvl.enemies.append(Enemy(2200, 492, 2060, 2500))
    lvl.enemies.append(Enemy(2400, 492, 2060, 2500))
    lvl.enemies.append(Enemy(2900, 492, 2760, 3400))
    lvl.enemies.append(Enemy(3200, 492, 2760, 3500))

    lvl.flag = (3500, 420)

    lvl.decor = [
        (150, 90, 1), (550, 60, 1), (1000, 110, 1),
        (1500, 70, 1), (2000, 100, 1), (2500, 60, 1),
        (3000, 90, 1), (3400, 70, 1)
    ]
    return lvl


def check_collisions(player, level, state):
    for c in level.coins:
        if not c.collected and player.rect.colliderect(c.rect):
            c.collected = True
            state["score"] += 10

    for e in level.enemies:
        if not e.alive:
            continue
        if player.rect.colliderect(e.rect):
            if player.vy > 0 and player.rect.bottom < e.rect.centery + 10:
                e.alive = False
                e.squash_timer = 30
                player.vy = -10
                state["score"] += 20
            else:
                state["lives"] -= 1
                return True
    return False


def draw_hud(surf, state, level_name):
    score_text = FONT.render(f"Score: {state['score']}", True, WHITE)
    lives_text = FONT.render(f"Lives: {state['lives']}", True, WHITE)
    lvl_text = SMALL_FONT.render(level_name, True, WHITE)
    surf.blit(score_text, (20, 10))
    surf.blit(lives_text, (20, 50))
    surf.blit(lvl_text, (WIDTH - 180, 15))


def show_message(surf, lines, color=WHITE):
    surf.fill(SKY)
    for i, line in enumerate(lines):
        text = FONT.render(line, True, color)
        surf.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 50))
    pygame.display.flip()


def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        clock.tick(30)


def run_level(level, state):
    player = Player(*level.spawn)
    cam_x = 0
    running = True
    hurt_timer = 0

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"

        if hurt_timer > 0:
            hurt_timer -= 1
            if hurt_timer == 0:
                if state["lives"] <= 0:
                    return "gameover"
                player = Player(*level.spawn)
                cam_x = 0
                hurt_timer = 0
        else:
            player.update(level.platforms)

            for e in level.enemies:
                e.update(level.platforms)
            for c in level.coins:
                c.update()

            if check_collisions(player, level, state):
                hurt_timer = 60

            if player.rect.top > HEIGHT + 100:
                state["lives"] -= 1
                if state["lives"] <= 0:
                    return "gameover"
                player = Player(*level.spawn)
                cam_x = 0

            target_cam = player.rect.centerx - WIDTH // 2
            cam_x += (target_cam - cam_x) * 0.1
            cam_x = max(0, min(cam_x, level.width - WIDTH))

            if level.flag:
                flag_rect = pygame.Rect(level.flag[0], level.flag[1], 50, 100)
                if player.rect.colliderect(flag_rect):
                    return "won"

        level.draw(screen, int(cam_x))
        player.draw(screen, int(cam_x))
        draw_hud(screen, state, level.name)

        if hurt_timer > 0 and (hurt_timer // 5) % 2 == 0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(100)
            overlay.fill(RED)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()

    return "quit"


def main():
    state = {"score": 0, "lives": 3}
    levels = [build_level1(), build_level2()]
    current = 0

    while True:
        result = run_level(levels[current], state)

        if result == "quit":
            break
        elif result == "gameover":
            show_message(screen, ["GAME OVER", f"Score: {state['score']}", "Press any key"], RED)
            wait_for_key()
            break
        elif result == "won":
            if current == 0:
                show_message(screen, ["LEVEL 1 COMPLETE!",
                                      f"Score: {state['score']}",
                                      "Press any key for next level"])
                wait_for_key()
                current = 1
            else:
                show_message(screen, ["CONGRATULATIONS!",
                                      "You beat all levels!",
                                      f"Final score: {state['score']}",
                                      "Press any key to exit"], YELLOW)
                wait_for_key()
                break

    pygame.quit()


if __name__ == "__main__":
    main()