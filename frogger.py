"""Frogger: cross the road and reach the top without being hit."""
import random
import pygame

W,H=640,600
LANES=[(420,3),(360,-4),(300,3),(240,-3),(180,4)]

def main():
    pygame.init()
    screen=pygame.display.set_mode((W,H)); pygame.display.set_caption("Frogger")
    clock=pygame.time.Clock(); font=pygame.font.Font(None,32)
    frog=pygame.Rect(W//2-14,H-42,28,28)
    cars=[]
    for lane,(y,speed) in enumerate(LANES):
        for i in range(3):
            cars.append([pygame.Rect(i*250+lane*50,y,65,30),speed])
    score=0; running=True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: running=False
                if e.key==pygame.K_UP: frog.y-=40
                if e.key==pygame.K_DOWN: frog.y+=40
                if e.key==pygame.K_LEFT: frog.x-=40
                if e.key==pygame.K_RIGHT: frog.x+=40
        frog.clamp_ip(screen.get_rect())
        for car,speed in cars:
            car.x+=speed
            if speed>0 and car.left>W: car.right=0
            if speed<0 and car.right<0: car.left=W
            if frog.colliderect(car): frog.topleft=(W//2-14,H-42); score=max(0,score-1)
        if frog.top<30: score+=1; frog.topleft=(W//2-14,H-42)
        screen.fill((25,90,55))
        pygame.draw.rect(screen,(55,55,60),(0,150,W,330))
        for y in [210,270,330,390,450]: pygame.draw.line(screen,(230,220,150),(0,y),(W,y),2)
        for car,_ in cars: pygame.draw.rect(screen,(220,80,70),car,border_radius=6)
        pygame.draw.rect(screen,(90,240,110),frog,border_radius=8)
        screen.blit(font.render(f"Crossings: {score}   Arrow keys",True,(255,255,255)),(12,12))
        pygame.display.flip()
    pygame.quit()

if __name__=="__main__": main()
