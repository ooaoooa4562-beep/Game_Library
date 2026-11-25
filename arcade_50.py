import math
import random
import pygame

# Fifty bite-sized arcade challenges. Run: python arcade_50.py
pygame.init()
W, H = 900, 620
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("ARCADE 50")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 22)
BIG = pygame.font.SysFont("arial", 42, bold=True)
WHITE=(240,245,255); BG=(12,17,30); BLUE=(55,155,255); RED=(245,80,90); GOLD=(255,205,70); GREEN=(70,220,150)

NAMES = [
"Neon Dodge","Meteor Run","Laser Alley","Bubble Collector","Coin Rush",
"Gem Sprint","Star Catcher","Orb Hunter","Gold Fever","Crystal Cave",
"Sky Defender","Alien Patrol","Astro Blaster","Robot Uprising","Target Practice",
"Rapid Fire","Cannon Storm","UFO Hunter","Pixel Sniper","Comet Breaker",
"Survival 60","Last One Standing","Red Zone","Electric Storm","Endless Fall",
"Shadow Escape","Ghost Corridor","Jungle Dash","Cave Runner","Lava Escape",
"Speed Gates","Color Switch","Moving Walls","Narrow Passage","Pulse Runner",
"Treasure Maze","Key Quest","Labyrinth 2D","Lost Temple","Exit Finder",
"Grid Master","Snake Arena","Tunnel Rush","Paddle Pop","Brick Storm",
"Falling Blocks","Meteor Miner","Space Courier","Rocket Landing","Final Orbit"
]
# Each entry has its own speed, target, palette and challenge parameters.
SPECS=[]
for i,name in enumerate(NAMES):
    kind=i%5
    SPECS.append({"name":name,"kind":kind,"speed":2.2+(i%7)*0.48,
                  "target":12+(i%6)*4,"color":[BLUE,GOLD,GREEN,RED,(180,120,255)][kind],
                  "seed":i*37+11})

def text(msg,x,y,font=FONT,color=WHITE):
    screen.blit(font.render(msg,True,color),(x,y))

def menu():
    selected=0
    while True:
        screen.fill(BG)
        text("ARCADE 50",35,22,BIG,GOLD)
        text("Choose a challenge  |  UP/DOWN or mouse  |  ENTER to play  |  ESC to quit",38,78)
        for row in range(10):
            for col in range(5):
                idx=row*5+col
                x=38+col*172; y=125+row*46
                rect=pygame.Rect(x,y,158,36)
                pygame.draw.rect(screen,(36,55,82) if idx!=selected else (45,105,155),rect,border_radius=7)
                pygame.draw.rect(screen,(75,105,140),rect,1,border_radius=7)
                label=f"{idx+1:02d}. {NAMES[idx]}"
                screen.blit(pygame.font.SysFont("arial",15,bold=True).render(label,True,WHITE),(x+7,y+9))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: return None
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:return None
                if e.key==pygame.K_UP:selected=(selected-1)%50
                if e.key==pygame.K_DOWN:selected=(selected+1)%50
                if e.key==pygame.K_LEFT:selected=(selected-10)%50
                if e.key==pygame.K_RIGHT:selected=(selected+10)%50
                if e.key in (pygame.K_RETURN,pygame.K_SPACE):return selected
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                for idx in range(50):
                    rect=pygame.Rect(38+(idx%5)*172,125+(idx//5)*46,158,36)
                    if rect.collidepoint(e.pos):return idx

def play(index):
    spec=SPECS[index]; rng=random.Random(spec["seed"])
    px,py=W//2,H-75; player=pygame.Rect(px,py,28,28)
    objects=[]; shots=[]; score=0; lives=3; tick=0; won=False; lost=False
    kind=spec["kind"]; speed=spec["speed"]; target=spec["target"]
    while True:
        dt=clock.tick(60); tick+=1
        for e in pygame.event.get():
            if e.type==pygame.QUIT:return False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:return True
                if e.key==pygame.K_r:return True
                if e.key==pygame.K_SPACE and kind in (2,4):shots.append(pygame.Rect(player.centerx-4,player.top-12,8,18))
        keys=pygame.key.get_pressed()
        if not (won or lost):
            dx=(keys[pygame.K_RIGHT] or keys[pygame.K_d])-(keys[pygame.K_LEFT] or keys[pygame.K_a])
            dy=(keys[pygame.K_DOWN] or keys[pygame.K_s])-(keys[pygame.K_UP] or keys[pygame.K_w])
            player.x+=int(dx*5); player.y+=int(dy*5)
            player.clamp_ip(screen.get_rect().inflate(-24,-24))
            if tick%max(12,int(42-speed*4))==0:
                x=rng.randint(35,W-55); size=rng.randint(18,34)
                # kind 0 dodge, 1 collect, 2 shoot, 3 survive, 4 precision
                good=(kind==1 and rng.random()<0.72) or (kind==4 and rng.random()<0.30)
                objects.append([pygame.Rect(x,-size,size,size),good,rng.choice([-1,0,1])])
            for obj in objects:
                r,good,drift=obj
                r.y+=int(speed+(score//8)*0.12)
                if kind==1 and good or kind==4 and good:r.x+=drift*2
                if r.colliderect(player):
                    if good:score+=2
                    else:lives-=1
                    r.y=H+100
                elif r.top>H:
                    if kind in (1,4) and good: lives-=1
                    elif kind in (0,2,3):score+=1
                    r.y=H+100
            objects=[o for o in objects if o[0].top<H+10]
            for shot in shots:
                shot.y-=9
                for obj in objects:
                    if shot.colliderect(obj[0]):
                        obj[0].y=H+100; shot.y=-100; score+=2
            shots=[s for s in shots if s.bottom>0]
            if score>=target:won=True
            if lives<=0:lost=True
        screen.fill(BG)
        # scrolling grid gives each challenge an arcade arena feel
        for x in range(0,W,50):pygame.draw.line(screen,(23,34,54),(x,0),(x,H))
        for y in range((tick//3)%50,H,50):pygame.draw.line(screen,(23,34,54),(0,y),(W,y))
        pygame.draw.rect(screen,spec["color"],player,border_radius=7)
        pygame.draw.rect(screen,WHITE,player,2,border_radius=7)
        for r,good,_ in objects:
            pygame.draw.rect(screen,GREEN if good else RED,r,border_radius=6)
            pygame.draw.circle(screen,(255,255,255),r.center,3)
        for s in shots:pygame.draw.rect(screen,GOLD,s,border_radius=3)
        text(f"{index+1:02d}  {spec['name']}",24,18,BIG)
        text(f"Score: {score}/{target}     Lives: {lives}",26,72,FONT,GOLD)
        text("Move: WASD / arrows     Fire: SPACE (shooting games)     R: menu     ESC: menu",24,H-34,FONT)
        if won or lost:
            pygame.draw.rect(screen,(10,15,27),(190,220,520,170),border_radius=16)
            text("CHALLENGE COMPLETE!" if won else "GAME OVER",285,245,BIG,GREEN if won else RED)
            text(f"Final score: {score}     Press R or ESC for the game list",260,315)
        pygame.display.flip()

def main():
    while True:
        choice=menu()
        if choice is None:break
        play(choice)
    pygame.quit()

if __name__=="__main__":main()
