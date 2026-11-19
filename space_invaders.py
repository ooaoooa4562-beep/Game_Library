"""Space Invaders: move, shoot and clear the alien formation."""
import pygame
import random

WIDTH, HEIGHT = 720, 560
WHITE, GREEN, RED, BLACK = (245,245,245), (70,230,120), (240,80,80), (8,12,28)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock, font = pygame.time.Clock(), pygame.font.Font(None,32)
    player = pygame.Rect(WIDTH//2-25, HEIGHT-55, 50, 24)
    aliens = [pygame.Rect(55+c*65,45+r*48,34,25) for r in range(4) for c in range(9)]
    shots, bombs = [], []
    direction, score, lives, cooldown = 1, 0, 3, 0
    running = True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and cooldown == 0:
                shots.append(pygame.Rect(player.centerx-3,player.top-12,6,14)); cooldown=14
        keys = pygame.key.get_pressed()
        player.x += (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])*6
        player.clamp_ip(screen.get_rect())
        cooldown = max(0,cooldown-1)
        for shot in shots[:]:
            shot.y -= 9
            if shot.bottom < 0: shots.remove(shot); continue
            hit = next((a for a in aliens if shot.colliderect(a)),None)
            if hit: aliens.remove(hit); shots.remove(shot); score += 10
        for alien in aliens: alien.x += direction*1
        if aliens and (min(a.left for a in aliens)<8 or max(a.right for a in aliens)>WIDTH-8):
            direction *= -1
            for alien in aliens: alien.y += 18
        if random.randrange(90)==0 and aliens: bombs.append(pygame.Rect(random.choice(aliens).centerx,80,5,14))
        for bomb in bombs[:]:
            bomb.y += 5
            if bomb.colliderect(player): bombs.remove(bomb); lives -= 1
            elif bomb.top>HEIGHT: bombs.remove(bomb)
        if any(a.bottom >= player.top for a in aliens) or lives <= 0: running = False
        screen.fill(BLACK)
        pygame.draw.rect(screen,GREEN,player,border_radius=6)
        for alien in aliens: pygame.draw.rect(screen,RED,alien,border_radius=5)
        for shot in shots: pygame.draw.rect(screen,WHITE,shot)
        for bomb in bombs: pygame.draw.rect(screen,(255,190,60),bomb)
        screen.blit(font.render(f"Score: {score}   Lives: {lives}   SPACE: fire",True,WHITE),(12,12))
        if not aliens: running = False
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__": main()
