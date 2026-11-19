"""Reusable, hand-drawn pixel-art sprites for the Game Library."""
import math
import pygame

def _shade(color, amount):
    return tuple(max(0, min(255, int(channel * amount))) for channel in color)

def draw_mario(surface, x, y, facing=1, frame=0):
    # A compact platform hero with cap, face, overalls, gloves and animated boots.
    bob = 1 if frame % 12 < 6 else 0
    pygame.draw.ellipse(surface, (45, 45, 65), (x+3, y+36, 28, 7))
    pygame.draw.rect(surface, (190, 35, 35), (x+4, y+2+bob, 25, 9), border_radius=4)
    pygame.draw.rect(surface, (145, 20, 25), (x+2, y+8+bob, 29, 5), border_radius=2)
    pygame.draw.ellipse(surface, (246, 190, 145), (x+7, y+8+bob, 19, 17))
    eye = x + (20 if facing > 0 else 9)
    pygame.draw.ellipse(surface, (255,255,255), (eye-2, y+13+bob, 5, 7))
    pygame.draw.circle(surface, (25,25,35), (eye+1, y+17+bob), 2)
    pygame.draw.arc(surface, (110,55,35), (x+10,y+17+bob,13,7), math.pi, math.tau, 2)
    pygame.draw.rect(surface, (30,75,190), (x+5,y+23+bob,23,14), border_radius=4)
    pygame.draw.rect(surface, (245,190,40), (x+9,y+24+bob,5,5), border_radius=2)
    pygame.draw.rect(surface, (245,190,40), (x+20,y+24+bob,5,5), border_radius=2)
    step = (frame//5)%2*3 if frame else 0
    pygame.draw.rect(surface, (245,190,145), (x+1,y+25+bob,5,9), border_radius=2)
    pygame.draw.rect(surface, (245,190,145), (x+27,y+25+bob,5,9), border_radius=2)
    pygame.draw.rect(surface, (90,45,35), (x+5+step,y+36,10,5), border_radius=2)
    pygame.draw.rect(surface, (90,45,35), (x+18-step,y+36,11,5), border_radius=2)

def draw_goomba(surface, rect):
    x,y=rect.topleft; w,h=rect.size
    pygame.draw.ellipse(surface,(70,35,20),(x,y+5,w,h-5))
    pygame.draw.ellipse(surface,(155,95,50),(x+2,y,w-4,h-8))
    pygame.draw.ellipse(surface,(245,225,190),(x+5,y+9,7,9))
    pygame.draw.ellipse(surface,(245,225,190),(x+w-12,y+9,7,9))
    pygame.draw.circle(surface,(20,15,15),(x+9,y+14),2)
    pygame.draw.circle(surface,(20,15,15),(x+w-9,y+14),2)
    pygame.draw.arc(surface,(45,20,15),(x+8,y+16,w-16,8),0,math.pi,2)
    pygame.draw.ellipse(surface,(45,25,20),(x+1,y+h-7,12,7))
    pygame.draw.ellipse(surface,(45,25,20),(x+w-13,y+h-7,12,7))

def draw_pacman(surface, center, radius, direction=(1,0), frame=0):
    cx,cy=center
    pygame.draw.circle(surface,(110,75,15),(cx+2,cy+3),radius)
    pygame.draw.circle(surface,(255,220,25),(cx,cy),radius)
    mouth=0.18+0.22*(0.5+0.5*math.sin(frame*0.35))
    angle=math.atan2(direction[1],direction[0])
    p1=(cx+math.cos(angle-mouth)*radius,cy+math.sin(angle-mouth)*radius)
    p2=(cx+math.cos(angle+mouth)*radius,cy+math.sin(angle+mouth)*radius)
    pygame.draw.polygon(surface,(5,5,20),[(cx,cy),p1,p2])
    pygame.draw.circle(surface,(255,255,255),(cx+int(math.cos(angle-0.8)*radius*.25),cy+int(math.sin(angle-0.8)*radius*.25)),2)

def draw_ghost(surface, rect, color=(235,65,95)):
    x,y=rect.topleft; w,h=rect.size
    pygame.draw.ellipse(surface,_shade(color,.55),(x+2,y+2,w-4,h-2))
    pygame.draw.rect(surface,color,(x+1,y+h//2,w-2,h//2))
    pygame.draw.arc(surface,_shade(color,1.2),(x+1,y,w-2,h),math.pi,math.tau,2)
    for i in range(3):
        px=x+i*w/3
        pygame.draw.polygon(surface,color,[(px,y+h-5),(px+w/6,y+h-1),(px+w/3,y+h-5)])
    for ex in (x+w*.34,x+w*.68):
        pygame.draw.ellipse(surface,(255,255,255),(int(ex-4),y+h*.38,8,10))
        pygame.draw.circle(surface,(25,50,100),(int(ex),int(y+h*.44)),2)

def draw_invader(surface, rect, frame=0):
    x,y=rect.topleft; w,h=rect.size
    c=(100,245,150)
    pygame.draw.rect(surface,c,(x+w*.2,y+h*.18,w*.6,h*.62),border_radius=4)
    pygame.draw.rect(surface,_shade(c,.7),(x+w*.05,y+h*.38,w*.9,h*.32),border_radius=3)
    for ex in (x+w*.34,x+w*.66):
        pygame.draw.rect(surface,(8,25,25),(int(ex-2),int(y+h*.35),4,5))
    leg=2 if frame%2 else 0
    pygame.draw.line(surface,c,(x+w*.28,y+h*.72),(x+w*.16,y+h-leg),3)
    pygame.draw.line(surface,c,(x+w*.72,y+h*.72),(x+w*.84,y+h-leg),3)
    pygame.draw.line(surface,c,(x+w*.08,y+h*.42),(x,y+h*.22),3)
    pygame.draw.line(surface,c,(x+w*.92,y+h*.42),(x+w,y+h*.22),3)

def draw_player_ship(surface, rect):
    x,y=rect.topleft; w,h=rect.size
    pygame.draw.polygon(surface,(30,80,105),[(x+w*.5,y),(x+w*.92,y+h*.9),(x+w*.5,y+h*.72),(x+w*.08,y+h*.9)])
    pygame.draw.polygon(surface,(80,235,190),[(x+w*.5,y+2),(x+w*.73,y+h*.78),(x+w*.5,y+h*.62),(x+w*.27,y+h*.78)])
    pygame.draw.ellipse(surface,(180,245,255),(x+w*.39,y+h*.28,w*.22,h*.25))
    pygame.draw.polygon(surface,(255,150,65),[(x+w*.36,y+h*.82),(x+w*.5,y+h*1.2),(x+w*.64,y+h*.82)])

def draw_car(surface, rect, color=(220,70,65)):
    x,y=rect.topleft; w,h=rect.size
    pygame.draw.ellipse(surface,(10,15,18),(x+2,y+h-5,w-4,8))
    pygame.draw.rect(surface,_shade(color,.65),(x+w*.06,y+h*.42,w*.88,h*.42),border_radius=5)
    pygame.draw.polygon(surface,color,[(x+w*.2,y+h*.48),(x+w*.34,y+h*.12),(x+w*.72,y+h*.12),(x+w*.88,y+h*.48)])
    pygame.draw.polygon(surface,(125,205,225),[(x+w*.37,y+h*.2),(x+w*.7,y+h*.2),(x+w*.8,y+h*.45),(x+w*.29,y+h*.45)])
    pygame.draw.line(surface,(65,75,85),(x+w*.54,y+h*.2),(x+w*.54,y+h*.46),2)
    for wx in (x+w*.24,x+w*.72):
        pygame.draw.circle(surface,(20,22,28),(int(wx),y+h-2),max(4,int(h*.19)))
        pygame.draw.circle(surface,(170,180,190),(int(wx),y+h-2),max(2,int(h*.08)))
    pygame.draw.rect(surface,(255,240,170),(x+w*.82,y+h*.52,4,4),border_radius=1)

def draw_frog(surface, rect, frame=0):
    x,y=rect.topleft; w,h=rect.size
    pygame.draw.ellipse(surface,(20,55,35),(x+2,y+h*.72,w-4,h*.22))
    pygame.draw.ellipse(surface,(45,175,75),(x+w*.12,y+h*.28,w*.76,h*.62))
    for ex in (x+w*.3,x+w*.7):
        pygame.draw.circle(surface,(65,195,85),(int(ex),int(y+h*.25)),int(w*.18))
        pygame.draw.circle(surface,(245,245,225),(int(ex),int(y+h*.23)),max(3,int(w*.11)))
        pygame.draw.circle(surface,(15,25,20),(int(ex+2),int(y+h*.23)),max(2,int(w*.055)))
    pygame.draw.arc(surface,(15,80,35),(x+w*.3,y+h*.45,w*.4,h*.25),0,math.pi,2)
    for fx in (x+w*.12,x+w*.68):
        pygame.draw.ellipse(surface,(65,195,85),(fx,y+h*.72,w*.22,h*.2))

def draw_crate(surface, rect):
    x,y=rect.topleft; w,h=rect.size
    pygame.draw.rect(surface,(80,42,20),(x+3,y+4,w-4,h-3),border_radius=4)
    pygame.draw.rect(surface,(170,105,52),(x,y,w-4,h-5),border_radius=4)
    pygame.draw.rect(surface,(225,165,95),(x+4,y+4,w-12,h-13),3,border_radius=2)
    pygame.draw.line(surface,(105,60,30),(x+6,y+6),(x+w-9,y+h-10),4)
    pygame.draw.line(surface,(105,60,30),(x+w-10,y+6),(x+6,y+h-10),4)
    pygame.draw.circle(surface,(235,185,115),(x+w//2,y+h//2),3)

def draw_sokoban_player(surface, center, radius=19):
    x,y=center
    pygame.draw.ellipse(surface,(10,20,30),(x-radius,y+radius-5,x*0+radius*2,8))
    pygame.draw.circle(surface,(35,115,150),(x,y),radius)
    pygame.draw.circle(surface,(80,205,235),(x-3,y-4),radius-4)
    pygame.draw.circle(surface,(245,215,175),(x,y-4),radius//2)
    pygame.draw.circle(surface,(25,35,45),(x-5,y-6),2)
    pygame.draw.circle(surface,(25,35,45),(x+5,y-6),2)
    pygame.draw.arc(surface,(70,45,35),(x-6,y-2,12,9),0,math.pi,2)

def draw_asteroid(surface, center, radius, seed=0):
    x,y=center
    points=[]
    for i in range(10):
        a=math.tau*i/10
        r=radius*(.78+.2*math.sin(i*2.7+seed))
        points.append((int(x+math.cos(a)*r),int(y+math.sin(a)*r)))
    pygame.draw.polygon(surface,(65,72,88),points)
    pygame.draw.polygon(surface,(145,153,168),points,3)
    pygame.draw.circle(surface,(95,103,120),(int(x-radius*.25),int(y-radius*.2)),max(3,radius//5))
    pygame.draw.circle(surface,(45,52,66),(int(x+radius*.28),int(y+radius*.22)),max(2,radius//7))

def draw_tetris_block(surface, x, y, color, size):
    rect=pygame.Rect(x+1,y+1,size-2,size-2)
    pygame.draw.rect(surface,_shade(color,.48),rect,border_radius=4)
    pygame.draw.rect(surface,color,(x+3,y+3,size-6,size-6),border_radius=3)
    pygame.draw.polygon(surface,_shade(color,1.35),[(x+4,y+4),(x+size-4,y+4),(x+size-8,y+8),(x+8,y+8)])
    pygame.draw.line(surface,(255,255,255),(x+5,y+5),(x+size-6,y+5),2)
    pygame.draw.line(surface,_shade(color,.55),(x+size-5,y+7),(x+size-5,y+size-5),2)

def draw_snake_segment(surface, rect, head=False, direction=(1,0)):
    x,y,w,h=rect
    pygame.draw.ellipse(surface,(5,25,20),(x+2,y+3,w-3,h-3))
    color=(80,235,115) if head else (30,155,85)
    pygame.draw.rect(surface,color,(x+1,y+1,w-2,h-2),border_radius=7)
    pygame.draw.line(surface,_shade(color,1.35),(x+5,y+4),(x+w-6,y+4),2)
    if head:
        ex=x+(w-7 if direction[0]>=0 else 5)
        ey=y+(5 if direction[1]>=0 else h-6)
        pygame.draw.circle(surface,(245,250,220),(ex,ey),3)
        pygame.draw.circle(surface,(15,25,20),(ex+1,ey),1)

def draw_mine_tile(surface, rect, opened=False):
    x,y,w,h=rect
    base=(105,115,130) if opened else (65,85,110)
    pygame.draw.rect(surface,(25,30,40),(x+1,y+2,w,h),border_radius=5)
    pygame.draw.rect(surface,base,(x,y,w-2,h-2),border_radius=5)
    if not opened:
        pygame.draw.line(surface,(145,165,190),(x+5,y+4),(x+w-7,y+4),2)
        pygame.draw.line(surface,(35,45,60),(x+5,y+h-6),(x+w-7,y+h-6),2)
    else:
        pygame.draw.rect(surface,_shade(base,.75),(x+3,y+3,w-8,h-8),1,border_radius=3)

def draw_flag(surface, center):
    x,y=center
    pygame.draw.line(surface,(225,230,240),(x,y-11),(x,y+11),2)
    pygame.draw.polygon(surface,(245,65,75),[(x+1,y-10),(x+11,y-7),(x+1,y-2)])
    pygame.draw.line(surface,(220,220,220),(x-5,y+11),(x+5,y+11),2)

def draw_mine(surface, center, radius=9):
    x,y=center
    pygame.draw.circle(surface,(20,22,28),(x,y),radius)
    for a in range(8):
        angle=math.tau*a/8
        pygame.draw.line(surface,(20,22,28),(x,y),(x+math.cos(angle)*(radius+4),y+math.sin(angle)*(radius+4)),2)
    pygame.draw.circle(surface,(210,215,225),(x-3,y-3),3)

def draw_paddle(surface, rect, color=(80,210,240)):
    pygame.draw.rect(surface,(20,35,55),(rect.x,rect.y+3,rect.w,rect.h),border_radius=8)
    pygame.draw.rect(surface,_shade(color,.65),rect,border_radius=8)
    pygame.draw.rect(surface,color,(rect.x+3,rect.y+2,rect.w-6,max(3,rect.h//3)),border_radius=6)

def draw_ball(surface, rect, color=(255,235,100)):
    pygame.draw.circle(surface,_shade(color,.5),rect.center,rect.width//2)
    pygame.draw.circle(surface,color,rect.center,max(2,rect.width//2-2))
    pygame.draw.circle(surface,(255,255,235),(rect.centerx-3,rect.centery-3),max(2,rect.width//5))

def draw_brick(surface, rect, color):
    pygame.draw.rect(surface,_shade(color,.5),rect,border_radius=4)
    pygame.draw.rect(surface,color,rect.inflate(-2,-2),border_radius=4)
    pygame.draw.line(surface,_shade(color,1.35),(rect.x+5,rect.y+4),(rect.right-5,rect.y+4),2)
    pygame.draw.line(surface,_shade(color,.55),(rect.x+5,rect.bottom-4),(rect.right-5,rect.bottom-4),2)

def draw_chess_piece(surface, center, color, kind):
    x,y=center
    light=color==(248,242,225)
    fill=(245,239,220) if light else (45,50,65)
    edge=(115,100,80) if light else (12,15,25)
    pygame.draw.ellipse(surface,(0,0,0,65),(x-24,y+20,48,10))
    pygame.draw.ellipse(surface,edge,(x-22,y+12,44,13))
    pygame.draw.ellipse(surface,fill,(x-20,y+8,40,11))
    if kind=="P":
        pygame.draw.circle(surface,fill,(x,y-12),9); pygame.draw.circle(surface,edge,(x,y-12),9,2)
        pygame.draw.polygon(surface,fill,[(x-8,y+8),(x-5,y-5),(x+5,y-5),(x+8,y+8)])
    elif kind=="R":
        pygame.draw.rect(surface,fill,(x-13,y-19,26,29)); pygame.draw.rect(surface,edge,(x-13,y-19,26,29),2)
        for dx in (-10,0,10): pygame.draw.rect(surface,fill,(x+dx-4,y-25,8,8))
    elif kind=="N":
        pygame.draw.polygon(surface,fill,[(x-12,y+8),(x-9,y-13),(x+2,y-24),(x+15,y-15),(x+12,y+8)])
        pygame.draw.polygon(surface,edge,[(x-12,y+8),(x-9,y-13),(x+2,y-24),(x+15,y-15),(x+12,y+8)],2)
        pygame.draw.circle(surface,edge,(x+6,y-15),2)
    elif kind=="B":
        pygame.draw.polygon(surface,fill,[(x-13,y+8),(x-8,y-15),(x,y-24),(x+8,y-15),(x+13,y+8)])
        pygame.draw.line(surface,edge,(x-4,y-17),(x+5,y-7),2)
    elif kind=="Q":
        pygame.draw.polygon(surface,fill,[(x-16,y+8),(x-11,y-13),(x,y-4),(x+11,y-13),(x+16,y+8)])
        for dx in (-12,0,12): pygame.draw.circle(surface,fill,(x+dx,y-18),4)
    else:
        pygame.draw.rect(surface,fill,(x-13,y-7,26,16))
        pygame.draw.rect(surface,fill,(x-6,y-26,12,20))
        pygame.draw.circle(surface,fill,(x,y-28),7)
        pygame.draw.line(surface,edge,(x,y-34),(x,y-17),2)
        pygame.draw.line(surface,edge,(x-8,y-26),(x+8,y-26),2)
    pygame.draw.line(surface,edge,(x-11,y+8),(x+11,y+8),2)

def draw_checker_piece(surface, center, side, king=False):
    x,y=center
    main=(205,65,58) if side==1 else (35,40,52)
    rim=(105,30,30) if side==1 else (10,12,20)
    pygame.draw.ellipse(surface,(0,0,0),(x-28,y+18,56,13))
    pygame.draw.ellipse(surface,rim,(x-27,y-25,54,54))
    pygame.draw.ellipse(surface,main,(x-25,y-29,50,50))
    pygame.draw.ellipse(surface,_shade(main,1.35),(x-19,y-24,38,12))
    pygame.draw.arc(surface,(245,225,190),(x-19,y-22,38,38),math.pi,math.tau,2)
    if king:
        pygame.draw.polygon(surface,(245,205,85),[(x-16,y+3),(x-20,y-11),(x-8,y-4),(x,y-17),(x+8,y-4),(x+20,y-11),(x+16,y+3)])
        pygame.draw.rect(surface,(245,205,85),(x-16,y+3,32,5))
