"""Chess board with legal move validation through python-chess."""
import sys
import pygame
from game_art import draw_chess_piece
try:
    import chess
except ImportError:
    print("Install dependency: pip install python-chess")
    sys.exit(1)

SIZE=640
PIECES={"P":"♙","N":"♘","B":"♗","R":"♖","Q":"♕","K":"♔",
        "p":"♟","n":"♞","b":"♝","r":"♜","q":"♛","k":"♚"}

def main():
    pygame.init()
    screen=pygame.display.set_mode((SIZE,SIZE+44)); pygame.display.set_caption("Chess")
    clock=pygame.time.Clock(); font=pygame.font.SysFont("segoeuisymbol",48); small=pygame.font.Font(None,28)
    board=chess.Board(); selected=None; running=True
    while running:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: running=False
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1 and e.pos[1]<SIZE and not board.is_game_over():
                file=e.pos[0]//80; rank=7-e.pos[1]//80; square=chess.square(file,rank)
                if selected is None: selected=square
                else:
                    move=chess.Move(selected,square)
                    if board.piece_at(selected) and board.piece_at(selected).piece_type==chess.PAWN and chess.square_rank(square) in (0,7):
                        move.promotion=chess.QUEEN
                    if move in board.legal_moves: board.push(move); selected=None
                    elif board.piece_at(square) and board.piece_at(square).color==board.turn: selected=square
                    else: selected=None
        for rank in range(8):
            for file in range(8):
                sq=chess.square(file,7-rank); rect=(file*80,rank*80,80,80)
                color=(238,216,181) if (rank+file)%2==0 else (125,85,60)
                pygame.draw.rect(screen,color,rect)
                if sq==selected: pygame.draw.rect(screen,(240,210,60),rect,4)
                piece=board.piece_at(sq)
                if piece:
                    piece_color=(248,242,225) if piece.color else (45,50,65)
                    draw_chess_piece(screen,(file*80+40,rank*80+40),piece_color,piece.symbol().upper())
        status="Game over: "+board.result() if board.is_game_over() else ("White" if board.turn else "Black")+" to move"
        screen.blit(small.render(status+"   Click a piece, then destination",True,(255,255,255)),(10,SIZE+12))
        pygame.display.flip(); clock.tick(30)
    pygame.quit()

if __name__=="__main__": main()
