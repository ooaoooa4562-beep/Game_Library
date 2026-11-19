"""Breakout: bounce the ball and destroy every brick."""
import pygame

WIDTH, HEIGHT = 720, 560

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Breakout")
    clock, font = pygame.time.Clock(), pygame.font.Font(None,32)
    paddle = pygame.Rect(WIDTH//2-55,HEIGHT-35,110,14)
    ball = pygame.Rect(WIDTH//2-8,HEIGHT//2,16,16)
    velocity = [4,-4]
    bricks = [pygame.Rect(12+c*70,55+r*28,64,20) for r in range(6) for c in range(10)]
    score, lives = 0, 3
    running = True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: running = False
        keys = pygame.key.get_pressed()
        paddle.x += (keys[pygame.K_RIGHT]-keys[pygame.K_LEFT])*8
        paddle.clamp_ip(screen.get_rect())
        ball.x += velocity[0]; ball.y += velocity[1]
        if ball.left<=0 or ball.right>=WIDTH: velocity[0] *= -1
        if ball.top<=0: velocity[1] = abs(velocity[1])
        if ball.colliderect(paddle) and velocity[1]>0:
            velocity[1] = -abs(velocity[1])
            velocity[0] += (ball.centerx-paddle.centerx)//18
        hit = next((brick for brick in bricks if ball.colliderect(brick)),None)
        if hit:
            bricks.remove(hit); velocity[1] *= -1; score += 10
        if ball.top>HEIGHT:
            lives -= 1; ball.center = (WIDTH//2,HEIGHT//2); velocity=[4,-4]
            if lives<=0: running=False
        screen.fill((12,16,32))
        pygame.draw.rect(screen,(80,210,240),paddle,border_radius=7)
        pygame.draw.ellipse(screen,(255,235,100),ball)
        for i,brick in enumerate(bricks):
            color=(230,90+i%4*35,90)
            pygame.draw.rect(screen,color,brick,border_radius=4)
        screen.blit(font.render(f"Score: {score}   Lives: {lives}",True,(245,245,245)),(12,12))
        if not bricks: running=False
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__": main()
