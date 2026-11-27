import os, subprocess, sys
os.environ["SDL_VIDEODRIVER"]="dummy"
os.environ["SDL_AUDIODRIVER"]="dummy"
games="zmeyka tetris pacman mario pong asteroids breakout space_invaders minesweeper tank_battle".split()
failed=[]
for game in games:
    code = """import pygame, runpy
original=pygame.event.get
frames=0
def events(*args, **kwargs):
    global frames
    frames+=1
    if frames>=35: return [pygame.event.Event(pygame.QUIT)]
    return original(*args, **kwargs)
pygame.event.get=events
runpy.run_path(%r,run_name='__main__')
""" % (game+".py")
    try:
        result=subprocess.run([sys.executable,"-c",code],timeout=20)
        print(game, "PASS" if result.returncode==0 else "FAIL",flush=True)
        if result.returncode: failed.append(game)
    except subprocess.TimeoutExpired:
        failed.append(game)
        print(game,"TIMEOUT",flush=True)
if failed: raise SystemExit("Failed: "+", ".join(failed))
