# Game Library

A collection of classic games written in Python with Pygame.

## Requirements

- Python 3.10 or newer
- Pygame

Install the main dependency:

```bash
python -m pip install pygame
```

Chess uses the separate `python-chess` rules engine:

```bash
python -m pip install python-chess
```

## Games

| File | Game | Controls |
|---|---|---|
| `mario.py` | Mario Platformer | Arrow keys / WASD, Space to jump |
| `tetris.py` | Tetris | See in-game instructions |
| `thirddrop.py` | Three Drop (match-three) | Mouse |
| `zmeyka.py` | Snake | WASD |
| `pacman.py` | Pac-Man | Arrow keys |
| `space_invaders.py` | Space Invaders | Left/Right, Space to fire |
| `breakout.py` | Breakout | Left/Right |
| `pong.py` | Pong (two players) | W/S and Up/Down |
| `minesweeper.py` | Minesweeper | Left click to reveal, right click to flag |
| `frogger.py` | Frogger | Arrow keys |
| `sokoban.py` | Sokoban | Arrow keys, Z to undo, R to reset |
| `chess.py` | Chess (two players) | Click a piece, then its destination |
| `checkers.py` | Checkers (two players) | Click a piece, then its destination |
| `asteroids.py` | Asteroids | Left/Right to rotate, Up to thrust, Space to shoot |

## Run a game

Open a terminal in this folder and run the file you want:

```bash
python pacman.py
```

Replace `pacman.py` with any game filename from the table.

## Artwork

- `game_art.py` contains shared hand-drawn sprites used by the games: characters, ghosts, vehicles, ships, gems, chess pieces, checkers, and arcade objects.
- `thirddrop.py` keeps its own detailed jewel-rendering system.
- Keep `game_art.py` beside the game scripts; the games import it directly.

## Notes

- Each game is launched as a standalone script; run one game at a time.
- Press Escape or close the game window to exit where supported.
- Chess promotes a pawn to a queen automatically.
- These projects are educational recreations of classic arcade and board-game mechanics.
