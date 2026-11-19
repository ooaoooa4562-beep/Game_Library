"""Sokoban: push every crate onto a goal. Undo with Z, reset with R."""
import pygame
from game_art import draw_crate, draw_sokoban_player

LEVEL=["##########","#   #    #","# $ # .  #","# $   .  #","#   ##   #","# .  $   #","#      @ #","##########"]
TILE=56

def main():
    pygame.init()
    screen=pygame.display.set_mode((len(LEVEL[0])*TILE,len(LEVEL)*TILE+48))
    pygame.display.set_caption("Sokoban")
    clock=pygame.time.Clock(); font=pygame.font.Font(None,30)
    def load():
        walls=set(); goals=set(); boxes=set(); player=[0,0]
        for y,row in enumerate(LEVEL):
            for x,c in enumerate(row):
                if c=="#": walls.add((x,y))
                if c==".": goals.add((x,y))
                if c=="$": boxes.add((x,y))
                if c=="@": player=[x,y]
        return walls,goals,boxes,player
    walls,goals,boxes,player=load(); history=[]; running=True
    while running:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: running=False
                if e.key==pygame.K_r: walls,goals,boxes,player=load(); history=[]
                if e.key==pygame.K_z and history: boxes,player=history.pop()
                moves={pygame.K_LEFT:(-1,0),pygame.K_RIGHT:(1,0),pygame.K_UP:(0,-1),pygame.K_DOWN:(0,1)}
                if e.key in moves:
                    dx,dy=moves[e.key]; target=(player[0]+dx,player[1]+dy); beyond=(target[0]+dx,target[1]+dy)
                    if target not in walls and (target not in boxes or (beyond not in walls and beyond not in boxes)):
                        history.append((boxes.copy(),player.copy()))
                        if target in boxes: boxes.remove(target); boxes.add(beyond)
                        player=[target[0],target[1]]
        screen.fill((25,28,38))
        for y,row in enumerate(LEVEL):
            for x,_ in enumerate(row):
                rect=(x*TILE,y*TILE,TILE-2,TILE-2); p=(x,y)
                color=(65,75,95) if p in walls else (38,45,55)
                pygame.draw.rect(screen,color,rect)
                if p in goals: pygame.draw.circle(screen,(230,190,70),(x*TILE+28,y*TILE+28),10)
        for x,y in boxes: draw_crate(screen,pygame.Rect(x*TILE+7,y*TILE+7,42,42))
        draw_sokoban_player(screen,(player[0]*TILE+28,player[1]*TILE+28))
        done=goals.issubset(boxes)
        screen.blit(font.render("Solved!" if done else "Arrows: move   Z: undo   R: reset",True,(255,255,255)),(10,len(LEVEL)*TILE+12))
        pygame.display.flip(); clock.tick(30)
    pygame.quit()

if __name__=="__main__": main()
