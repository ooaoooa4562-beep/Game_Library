import math
import random
import pygame

pygame.init()
W,H=960,640
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("TANK BATTLE")
clock=pygame.time.Clock()
FONT=pygame.font.SysFont("arial",22)
BIG=pygame.font.SysFont("arial",46,bold=True)
BG=(24,39,35); WHITE=(240,245,230); GREEN=(91,174,91); DARK=(38,75,49)
RED=(205,72,63); GOLD=(255,207,83); BLUE=(83,151,210)

def draw_tank(surface,x,y,angle,color):
    body=pygame.Surface((48,38),pygame.SRCALPHA)
    pygame.draw.rect(body,(20,25,20),(3,3,42,32),border_radius=8)
    pygame.draw.rect(body,color,(8,6,32,26),border_radius=6)
    pygame.draw.rect(body,(35,43,34),(18,10,12,18),border_radius=5)
    pygame.draw.circle(body,(175,195,145),(24,19),7)
    pygame.draw.rect(body,(40,45,38),(21,1,6,22),border_radius=3)
    rotated=pygame.transform.rotate(body,-angle)
    surface.blit(rotated,rotated.get_rect(center=(x,y)))

def round_game():
    random.seed()
    player=[W/2,H-85,0]
    enemies=[[random.randint(70,W-70),random.randint(70,260),180] for _ in range(5)]
    bullets=[]; enemy_bullets=[]; walls=[]
    for _ in range(16):
        x=random.randrange(50,W-90,40); y=random.randrange(90,H-120,40)
        candidate=pygame.Rect(x,y,random.choice([38,70]),34)
        if abs(x-W/2)>100 and not any(candidate.inflate(48,48).collidepoint(e[0],e[1]) for e in enemies):
            walls.append(candidate)
    hp=5; score=0; tick=0; game_over=False; victory=False
    while True:
        clock.tick(60); tick+=1
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();return
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:pygame.quit();return
                if e.key==pygame.K_r:
                    return True
                if e.key==pygame.K_SPACE and not game_over and not victory:
                    a=math.radians(player[2]); bullets.append([player[0]+math.sin(a)*29,player[1]-math.cos(a)*29,a,0])
        keys=pygame.key.get_pressed()
        if not game_over and not victory:
            old_position=player[:2]
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:player[2]=(player[2]+3)%360
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:player[2]=(player[2]-3)%360
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                a=math.radians(player[2]); player[0]+=math.sin(a)*2.7; player[1]-=math.cos(a)*2.7
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                a=math.radians(player[2]); player[0]-=math.sin(a)*1.6; player[1]+=math.cos(a)*1.6
            player[0]=max(28,min(W-28,player[0]));player[1]=max(28,min(H-28,player[1]))
            if any(w.inflate(40,40).collidepoint(*player[:2]) for w in walls):
                player[:2]=old_position
            for enemy in enemies:
                old_enemy=enemy[:2]
                dx=player[0]-enemy[0];dy=player[1]-enemy[1]
                enemy[2]=(math.degrees(math.atan2(dx,-dy)))%360
                dist=math.hypot(dx,dy)
                if dist>145:
                    a=math.radians(enemy[2]); enemy[0]+=math.sin(a)*0.85;enemy[1]-=math.cos(a)*0.85
                if any(w.inflate(40,40).collidepoint(*enemy[:2]) for w in walls):
                    enemy[:2]=old_enemy
                if tick%95==0:
                    a=math.radians(enemy[2]);enemy_bullets.append([enemy[0]+math.sin(a)*25,enemy[1]-math.cos(a)*25,a])
            for b in bullets:
                b[0]+=math.sin(b[2])*7;b[1]-=math.cos(b[2])*7
                for wall in walls:
                    if wall.collidepoint(b[0],b[1]):b[3]=1
                if b[3]: continue
                for enemy in enemies[:]:
                    if math.hypot(b[0]-enemy[0],b[1]-enemy[1])<24:
                        enemies.remove(enemy);score+=100;b[3]=1
                        break
            bullets=[b for b in bullets if -10<b[0]<W+10 and -10<b[1]<H+10 and not b[3]]
            for b in enemy_bullets:
                b[0]+=math.sin(b[2])*4;b[1]-=math.cos(b[2])*4
                if math.hypot(b[0]-player[0],b[1]-player[1])<22:
                    hp-=1;b[1]=H+100
                if any(w.collidepoint(b[0],b[1]) for w in walls):b[1]=H+100
            enemy_bullets=[b for b in enemy_bullets if -10<b[0]<W+10 and -10<b[1]<H+10]
            if hp<=0:game_over=True
            if not enemies:victory=True
        screen.fill(BG)
        for x in range(0,W,48):
            pygame.draw.line(screen,(34,54,46),(x,0),(x,H),1)
        for y in range(0,H,48):
            pygame.draw.line(screen,(34,54,46),(0,y),(W,y),1)
        for wall in walls:
            pygame.draw.rect(screen,(105,112,91),wall,border_radius=5)
            pygame.draw.rect(screen,(55,67,54),wall,3,border_radius=5)
            pygame.draw.line(screen,(145,150,123),wall.topleft,(wall.right,wall.top),2)
        draw_tank(screen,*player,GREEN)
        for enemy in enemies:draw_tank(screen,*enemy,RED)
        for b in bullets+enemy_bullets:
            pygame.draw.circle(screen,GOLD if b in bullets else (255,105,80),(int(b[0]),int(b[1])),5)
        pygame.draw.rect(screen,(15,22,20),(0,0,W,48))
        screen.blit(FONT.render(f"HP: {hp}     Score: {score}     Enemies left: {len(enemies)}",True,WHITE),(20,12))
        screen.blit(FONT.render("WASD / arrows: drive and turn     SPACE: fire     R: restart     ESC: quit",True,WHITE),(18,H-32))
        if game_over or victory:
            pygame.draw.rect(screen,(10,18,17),(210,220,540,170),border_radius=16)
            label="VICTORY!" if victory else "TANK DESTROYED"
            screen.blit(BIG.render(label,True,GOLD if victory else RED),(300,245))
            screen.blit(FONT.render("Press R to play again or ESC to quit",True,WHITE),(320,320))
        pygame.display.flip()

if __name__=="__main__":
    while round_game():
        pass
