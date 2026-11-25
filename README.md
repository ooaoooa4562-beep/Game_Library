# Game Library

A growing collection of Python games built with Pygame.

## Requirements

- Python 3.10+
- Pygame

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Classic games

| File | Game |
|---|---|
| `mario.py` | Mario Platformer |
| `tetris.py` | Tetris |
| `thirddrop.py` | Three Drop (match-three) |
| `zmeyka.py` | Snake |
| `pacman.py` | Pac-Man |
| `space_invaders.py` | Space Invaders |
| `breakout.py` | Breakout |
| `pong.py` | Pong |
| `minesweeper.py` | Minesweeper |
| `frogger.py` | Frogger |
| `sokoban.py` | Sokoban |
| `chess.py` | Chess (requires python-chess) |
| `checkers.py` | Checkers |
| `asteroids.py` | Asteroids |

## New additions

| File | Game | How to play |
|---|---|---|
| `arcade_50.py` | 50 mini-game arcade collection | Open the menu, choose one of 50 challenges, move with WASD/arrows; Space fires in shooting challenges |
| `tank_battle.py` | Tank Battle | WASD/arrows to drive and turn, Space to fire, R to restart |

The 50 challenges are launched from one menu-driven collection, so you do not need to open 50 separate Python files.

## Run

```bash
python tank_battle.py
python arcade_50.py
```

Or launch any classic game by running its Python file.

## Artwork

- `game_art.py` contains shared hand-drawn Pygame sprites.
- `thirddrop.py` has its own jewel-rendering system.
- Keep `game_art.py` beside the game scripts that import it.

Run one game at a time. Press Escape or close the window to exit.
