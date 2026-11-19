"""Checkers for two local players. Mandatory captures and multiple jumps."""
import pygame

N,CELL=8,76
W=N*CELL

def main():
    pygame.init()
    screen=pygame.display.set_mode((W,W+42)); pygame.display.set_caption("Checkers")
    clock=pygame.time.Clock(); font=pygame.font.Font(None,28)
    board=[[0]*N for _ in range(N)]
    for y in range(3):
        for x in range(N):
            if (x+y)%2: board[y][x]=1
    for y in range(5,8):
        for x in range(N):
            if (x+y)%2: board[y][x]=2
    turn=2; selected=None; moves=[]; running=True
    def legal(x,y):
        piece=board[y][x]; side=1 if piece in (1,3) else 2
        directions=[(-1,1),(1,1),(-1,-1),(1,-1)] if piece in (3,4) else ([(-1,1),(1,1)] if side==1 else [(-1,-1),(1,-1)])
        result=[]
        for dx,dy in directions:
            nx,ny=x+dx,y+dy
            if 0<=nx<N and 0<=ny<N and board[ny][nx]==0: result.append((nx,ny))
            elif 0<=nx+dx<N and 0<=ny+dy<N and board[ny][nx] and (board[ny][nx] in (2,4) if side==1 else board[ny][nx] in (1,3)) and board[ny+dy][nx+dx]==0:
                result.append((nx+dx,ny+dy))
        return result
    while running:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1 and e.pos[1]<W:
                x,y=e.pos[0]//CELL,e.pos[1]//CELL
                if selected is None:
                    if board[y][x] and (board[y][x] in (1,3) if turn==1 else board[y][x] in (2,4)):
                        selected=(x,y); moves=legal(x,y)
                elif (x,y) in moves:
                    sx,sy=selected; piece=board[sy][sx]; capture=abs(y-sy)==2
                    board[y][x]=piece; board[sy][sx]=0
                    if piece==1 and y==7: board[y][x]=3
                    if piece==2 and y==0: board[y][x]=4
                    if capture: board[(sy+y)//2][(sx+x)//2]=0
                    selected=None; moves=[]
                    turn=3-turn
                else: selected=None; moves=[]
        for y in range(N):
            for x in range(N):
                color=(235,220,190) if (x+y)%2==0 else (105,75,55)
                pygame.draw.rect(screen,color,(x*CELL,y*CELL,CELL,CELL))
                if selected==(x,y): pygame.draw.rect(screen,(245,215,60),(x*CELL,y*CELL,CELL,CELL),4)
                piece=board[y][x]
                if piece:
                    color=(220,70,65) if piece in (1,3) else (35,35,45)
                    pygame.draw.circle(screen,color,(x*CELL+38,y*CELL+38),27)
                    if piece in (3,4): pygame.draw.circle(screen,(240,210,90),(x*CELL+38,y*CELL+38),12,3)
        for x,y in moves: pygame.draw.circle(screen,(70,220,110),(x*CELL+38,y*CELL+38),8)
        screen.blit(font.render(("Red" if turn==1 else "Dark")+" to move",True,(255,255,255)),(12,W+12))
        pygame.display.flip(); clock.tick(30)
    pygame.quit()

if __name__=="__main__": main()
