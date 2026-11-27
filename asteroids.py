"""Asteroids: rotate, thrust and shoot to clear the field."""
import math
import random
import pygame
from game_art import draw_asteroid

W,H=800,600

def main():
    pygame.init()
    screen=pygame.display.set_mode((W,H)); pygame.display.set_caption("Asteroids")
    clock=pygame.time.Clock(); font=pygame.font.Font(None,30)
    ship=[W/2,H/2]; angle=0; velocity=[0.0,0.0]; bullets=[]; rocks=[]
    for _ in range(8):
        rocks.append([random.randrange(W),random.randrange(H),random.uniform(-2,2),random.uniform(-2,2),random.randint(24,38)])
    score=0; lives=3; cooldown=0; running=True; shield=120
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: running=False
                if e.key==pygame.K_SPACE and cooldown==0:
                    bullets.append([ship[0],ship[1],math.cos(angle)*8,math.sin(angle)*8]); cooldown=12
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: angle-=0.06
        if keys[pygame.K_RIGHT]: angle+=0.06
        if keys[pygame.K_UP]:
            velocity[0]+=math.cos(angle)*0.18; velocity[1]+=math.sin(angle)*0.18
        ship[0]=(ship[0]+velocity[0])%W; ship[1]=(ship[1]+velocity[1])%H
        velocity=[v*0.99 for v in velocity]; cooldown=max(0,cooldown-1)
        for bullet in bullets[:]:
            bullet[0]=(bullet[0]+bullet[2])%W; bullet[1]=(bullet[1]+bullet[3])%H
            if len(bullet) == 4: bullet.append(0)
            bullet[4] += 1
            if bullet[4]>70: bullets.remove(bullet); continue
            for rock in rocks[:]:
                if math.hypot(bullet[0]-rock[0],bullet[1]-rock[1])<rock[4]:
                    bullets.remove(bullet); rocks.remove(rock); score+=10
                    if rock[4]>25:
                        for _ in range(2): rocks.append([rock[0],rock[1],random.uniform(-3,3),random.uniform(-3,3),rock[4]*0.55])
                    break
        for rock in rocks:
            rock[0]=(rock[0]+rock[2])%W; rock[1]=(rock[1]+rock[3])%H
            if shield == 0 and math.hypot(ship[0]-rock[0],ship[1]-rock[1])<rock[4]+10:
                shield=120; lives-=1; ship=[W/2,H/2]; velocity=[0,0]
                if lives<=0: running=False
        shield=max(0,shield-1)
        screen.fill((5,7,18))
        tip=(ship[0]+math.cos(angle)*18,ship[1]+math.sin(angle)*18)
        left=(ship[0]+math.cos(angle+2.5)*15,ship[1]+math.sin(angle+2.5)*15)
        right=(ship[0]+math.cos(angle-2.5)*15,ship[1]+math.sin(angle-2.5)*15)
        pygame.draw.polygon(screen,(20,55,75),[tip,left,right])
        pygame.draw.polygon(screen,(235,245,255),[tip,left,right],2)
        pygame.draw.circle(screen,(80,200,235),(int(ship[0]),int(ship[1])),5)
        for index,(x,y,_,_,r) in enumerate(rocks): draw_asteroid(screen,(int(x),int(y)),int(r),index)
        for b in bullets: pygame.draw.circle(screen,(255,220,100),(int(b[0]),int(b[1])),3)
        screen.blit(font.render(f"Score: {score}   Lives: {lives}   Arrows + SPACE",True,(255,255,255)),(12,12))
        if not rocks: running=False
        pygame.display.flip()
    pygame.quit()

if __name__=="__main__": main()
