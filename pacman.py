"""Pac-Man: collect every dot while avoiding the ghosts."""
import random
import pygame
from game_art import draw_pacman, draw_ghost

TILE = 24
LEVEL = ["###################", "#........#........#", "#.##.###.#.###.##.#",
        "#o##..... .....##o#", "#.##.##.#.#.##.##.#", "#......# #......#",
        "####.#       #.####", "   #.# ## ## #.#   ", "####.# #   # #.####",
        "     . #   # .     ", "####.# ##### #.####", "   #.#       #.#   ",
        "####.# ##### #.####", "#........#........#", "#.##.###.#.###.##.#",
        "#o..#.........#...#", "###.#.##.#.##.#.###", "#.................#", "###################"]
ROWS, COLS = len(LEVEL), len(LEVEL[0])
W, H = COLS*TILE, ROWS*TILE+42
WALL, BG, YELLOW, WHITE, RED = (20,35,180), (5,5,20), (255,220,0), (240,240,240), (240,70,80)

def main():
    pygame.init()
    screen = pygame.display.set_mode((W,H))
    pygame.display.set_caption("Pac-Man")
    clock, font = pygame.time.Clock(), pygame.font.Font(None, 30)
    grid = [list(row.ljust(COLS)) for row in LEVEL]
    player = [1,1]; direction = (0,0); queued = (0,0)
    ghosts = [[COLS-2,1], [COLS-2,ROWS-2], [1,ROWS-2]]
    score, lives = 0, 3
    def open_cell(x,y): return 0 <= y < ROWS and 0 <= x < COLS and grid[y][x] != "#"
    running = True
    while running:
        clock.tick(9)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.KEYDOWN:
                queued = {pygame.K_LEFT:(-1,0), pygame.K_RIGHT:(1,0), pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1)}.get(e.key, queued)
                if e.key == pygame.K_ESCAPE: running = False
                if e.key == pygame.K_r: return main()
        if open_cell(player[0]+queued[0], player[1]+queued[1]): direction = queued
        nx, ny = player[0]+direction[0], player[1]+direction[1]
        if open_cell(nx,ny): player = [nx,ny]
        if grid[player[1]][player[0]] in ".o":
            score += 50 if grid[player[1]][player[0]] == "o" else 10
            grid[player[1]][player[0]] = " "
        for ghost in ghosts:
            options = [(ghost[0]+dx,ghost[1]+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if open_cell(ghost[0]+dx,ghost[1]+dy)]
            if options: ghost[:] = random.choice(options)
            if ghost == player:
                lives -= 1; player = [1,1]; direction = (0,0)
                if lives <= 0: running = False
        screen.fill(BG)
        for y,row in enumerate(grid):
            for x,c in enumerate(row):
                rect = (x*TILE,y*TILE,TILE,TILE)
                if c == "#": pygame.draw.rect(screen,WALL,rect,border_radius=4)
                elif c in ".o": pygame.draw.circle(screen,YELLOW,(x*TILE+12,y*TILE+12),3 if c=="." else 7)
        draw_pacman(screen, (player[0]*TILE+12, player[1]*TILE+12), 10, direction, pygame.time.get_ticks()//40)
        ghost_colors = [(245,65,95),(80,205,245),(245,150,220)]
        for index,(x,y) in enumerate(ghosts):
            draw_ghost(screen, pygame.Rect(x*TILE+2,y*TILE+2,20,20), ghost_colors[index%len(ghost_colors)])
        screen.blit(font.render(f"Score {score}    Lives {lives}    R: restart",True,WHITE),(8,H-32))
        if not any("." in row or "o" in row for row in grid): running = False
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__": main()
