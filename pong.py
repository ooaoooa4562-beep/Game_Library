"""Pong for two players. W/S and Up/Down control the paddles."""
import pygame

WIDTH, HEIGHT = 800, 500

def main():
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Pong")
    clock=pygame.time.Clock()
    font=pygame.font.Font(None,48)
    left=pygame.Rect(24,HEIGHT//2-48,14,96); right=pygame.Rect(WIDTH-38,HEIGHT//2-48,14,96)
    ball=pygame.Rect(WIDTH//2-10,HEIGHT//2-10,20,20)
    vx,vy=5,4; score=[0,0]; running=True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: running=False
        keys=pygame.key.get_pressed()
        left.y += (keys[pygame.K_s]-keys[pygame.K_w])*7
        right.y += (keys[pygame.K_DOWN]-keys[pygame.K_UP])*7
        left.clamp_ip(screen.get_rect()); right.clamp_ip(screen.get_rect())
        ball.x+=vx; ball.y+=vy
        if ball.top<=0 or ball.bottom>=HEIGHT: vy *= -1
        if ball.colliderect(left) and vx<0: vx=abs(vx); vy += (ball.centery-left.centery)//18
        if ball.colliderect(right) and vx>0: vx=-abs(vx); vy += (ball.centery-right.centery)//18
        if ball.left<0: score[1]+=1; ball.center=(WIDTH//2,HEIGHT//2); vx=5
        if ball.right>WIDTH: score[0]+=1; ball.center=(WIDTH//2,HEIGHT//2); vx=-5
        screen.fill((8,12,25))
        for y in range(0,HEIGHT,24): pygame.draw.rect(screen,(80,90,110),(WIDTH//2-2,y,4,12))
        pygame.draw.rect(screen,(240,240,240),left); pygame.draw.rect(screen,(240,240,240),right)
        pygame.draw.ellipse(screen,(255,220,90),ball)
        screen.blit(font.render(f"{score[0]}     {score[1]}",True,(255,255,255)),(WIDTH//2-75,18))
        pygame.display.flip()
    pygame.quit()

if __name__=="__main__": main()
