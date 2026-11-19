"""Minesweeper: left click to reveal, right click to flag."""
import random
import pygame

SIZE, CELL, MINES = 10, 42, 15

def main():
    pygame.init()
    screen=pygame.display.set_mode((SIZE*CELL,SIZE*CELL+70))
    pygame.display.set_caption("Minesweeper")
    clock=pygame.time.Clock(); font=pygame.font.Font(None,30)
    mines=set(random.sample([(x,y) for x in range(SIZE) for y in range(SIZE)],MINES))
    opened=set(); flags=set(); lost=False; won=False
    def neighbors(x,y):
        return [(x+dx,y+dy) for dx in (-1,0,1) for dy in (-1,0,1)
                if (dx or dy) and 0<=x+dx<SIZE and 0<=y+dy<SIZE]
    def reveal(x,y):
        if (x,y) in opened or (x,y) in flags: return
        opened.add((x,y))
        if (x,y) not in mines and sum(p in mines for p in neighbors(x,y))==0:
            for p in neighbors(x,y): reveal(*p)
    running=True
    while running:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            if e.type==pygame.MOUSEBUTTONDOWN and not (lost or won) and e.pos[1]<SIZE*CELL:
                x,y=e.pos[0]//CELL,e.pos[1]//CELL
                if e.button==3:
                    if (x,y) in flags: flags.remove((x,y))
                    else: flags.add((x,y))
                elif e.button==1:
                    if (x,y) in mines: lost=True
                    else: reveal(x,y)
        won=len(opened)==SIZE*SIZE-MINES
        screen.fill((28,34,44))
        for y in range(SIZE):
            for x in range(SIZE):
                p=(x,y); rect=(x*CELL,y*CELL,CELL-2,CELL-2)
                color=(95,105,120) if p in opened else (55,75,95)
                pygame.draw.rect(screen,color,rect,border_radius=4)
                if p in flags: text="⚑"
                elif p in mines and lost: text="*"
                elif p in opened:
                    count=sum(n in mines for n in neighbors(x,y)); text=str(count) if count else ""
                else: text=""
                if text: screen.blit(font.render(text,True,(255,220,90)),(x*CELL+14,y*CELL+10))
        status="You win!" if won else "Game over" if lost else f"Mines: {MINES}   Flags: {len(flags)}"
        screen.blit(font.render(status,True,(245,245,245)),(10,SIZE*CELL+18))
        pygame.display.flip(); clock.tick(30)
    pygame.quit()

if __name__=="__main__": main()
