"""Minesweeper: left click to reveal, right click to flag."""
import random
import pygame
from game_art import draw_mine_tile, draw_flag, draw_mine

SIZE, CELL, MINES = 10, 42, 15

def main():
    pygame.init()
    screen=pygame.display.set_mode((SIZE*CELL,SIZE*CELL+70))
    pygame.display.set_caption("Minesweeper")
    clock=pygame.time.Clock(); font=pygame.font.Font(None,30)
    mines=set(); started=None
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
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: running=False
                if e.key==pygame.K_r:
                    mines.clear(); opened.clear(); flags.clear(); lost=False; won=False; started=None
            if e.type==pygame.MOUSEBUTTONDOWN and not (lost or won) and e.pos[1]<SIZE*CELL:
                x,y=e.pos[0]//CELL,e.pos[1]//CELL
                if e.button==3:
                    if (x,y) in flags: flags.remove((x,y))
                    elif (x,y) not in opened and len(flags)<MINES: flags.add((x,y))
                elif e.button==1:
                    if (x,y) in flags: continue
                    if started is None:
                        safe=set(neighbors(x,y)) | {(x,y)}
                        mines.update(random.sample([(a,b) for a in range(SIZE) for b in range(SIZE) if (a,b) not in safe],MINES))
                        started=pygame.time.get_ticks()
                    if (x,y) in mines: lost=True
                    else: reveal(x,y)
        won=len(opened)==SIZE*SIZE-MINES
        screen.fill((28,34,44))
        for y in range(SIZE):
            for x in range(SIZE):
                p=(x,y); rect=(x*CELL,y*CELL,CELL-2,CELL-2)
                draw_mine_tile(screen,rect,p in opened)
                if p in flags:
                    draw_flag(screen,(x*CELL+CELL//2,y*CELL+CELL//2))
                elif p in mines and lost:
                    draw_mine(screen,(x*CELL+CELL//2,y*CELL+CELL//2),9)
                elif p in opened:
                    count=sum(n in mines for n in neighbors(x,y))
                    if count:
                        number_colors={1:(80,160,255),2:(80,190,100),3:(235,80,75),4:(130,90,210),5:(170,90,55),6:(60,180,180),7:(30,30,30),8:(120,120,120)}
                        label=font.render(str(count),True,number_colors[count])
                        screen.blit(label,label.get_rect(center=(x*CELL+CELL//2,y*CELL+CELL//2)))
        status="You win!" if won else "Game over" if lost else f"Mines: {MINES}   Flags: {len(flags)}"
        screen.blit(font.render(status,True,(245,245,245)),(10,SIZE*CELL+18))
        screen.blit(font.render('R: restart | ESC: exit',True,(190,200,215)),(10,SIZE*CELL+43))
        pygame.display.flip(); clock.tick(30)
    pygame.quit()

if __name__=="__main__": main()
