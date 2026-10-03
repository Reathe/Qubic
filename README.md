# Qubic: 3D Tic-Tac-Toe (4×4×4)

> A 3D connect-four / tic-tac-toe game in Python with a fully navigable 3D board, gravity, a NegaMax AI
> opponent, and online multiplayer through a custom TCP game server.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Ursina](https://img.shields.io/badge/Ursina-3D_engine-orange)
![Panda3D](https://img.shields.io/badge/Panda3D-informational)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

*Qubic* (also called *Morpion 3D*) is played on a **4 × 4 × 4 cube**. Players take turns dropping pieces,
which fall to the lowest free level of their column. The first to line up **4 pieces** in any direction wins:
along a row, a column, vertically, or along any of the 2D and 3D diagonals.

## Features

- **3D board** rendered with [Ursina](https://www.ursinaengine.org/) (built on Panda3D). The orbit camera
  can be rotated and zoomed with the mouse.
- **Three game modes:**
  - **1 vs 1** on the same machine
  - **1 vs AI**: who starts is decided at random
  - **Online**: create or join a game room on a server
- **NegaMax AI** with alpha-beta pruning (depth-limited search).
- **Keyboard and mouse controls.** Keyboard movement is relative to the camera angle, so "up" always means
  "away from you".
- **Client/server networking** over TCP, with a lobby of rooms that refreshes automatically.
- **Unit tests** for the game model, cursor, pieces and AI.

## Getting started

### Requirements

- Python 3.8+
- `git` (Ursina is installed from its repository)

```bash
git clone https://github.com/Reathe/Qubic
cd Qubic
pip install -r requirements.txt
python main.py
```

### Controls

| Input | Action |
| --- | --- |
| Arrow keys | Move the cursor (relative to the camera) |
| `Enter` / click a column | Drop a piece |
| Left mouse drag | Rotate the camera |
| Mouse wheel | Zoom |
| Top-left button | Back to the main menu |

### Playing online

The client connects to the server address set in `src/networking/client.py` (`HOST`, `PORT`). To host your
own server:

```bash
python main_server.py     # listens on TCP port 9999 and shows a live view of the games
```

Then set `HOST` in `src/networking/client.py` to that machine's address (e.g. `"localhost"`).

### Running the tests

```bash
PYTHONPATH=src python -m unittest discover -s tests/model
```

## Architecture

The code follows **MVC** and uses several classic design patterns:

```
src/
├── model/                 # Game logic, no UI dependency
│   ├── qubic.py           # Board state, gravity, move validation, win detection, undo
│   ├── ai.py              # AI strategies (NegaMax, Random), selected via settings
│   ├── curseur.py         # 3D cursor
│   └── pion.py            # Pieces
├── ui/                    # Views (Ursina entities)
│   ├── qubic/             # 3D board and pieces
│   ├── qamera/            # Orbit camera
│   └── menu/              # Main menu and online lobby
├── controls.py            # Controllers: local, local-vs-AI, online; keyboard and mouse inputs
├── game_modes.py          # Wires model + view + controller for each mode
├── qubic_observer.py      # Observer pattern: views react to model changes
└── networking/
    ├── server.py          # Threaded TCP server; requests handled by a Chain of Responsibility
    ├── rooms.py           # Room management (create / join / leave, full-room errors…)
    └── client.py          # Client: JSON (jsonpickle) request/response protocol
```

| Pattern | Where |
| --- | --- |
| **Observer** | The model notifies the views and controls of each move (`QubicSubject` / `QubicObserver`) |
| **Strategy** | Interchangeable AIs (`NegaMax`, `Random`) and controllers (local, AI, online) |
| **Chain of Responsibility** | Server request handlers (register, create room, join, play…) |
| **Composite** | UI component trees |

### How the AI works

`NegaMax` explores the game tree up to **depth 4**. It plays each legal move on the board, recurses, and undoes
the move (`annule_coup`), so the board is never copied at every node. Wins are scored ±64, and branches that
cannot beat the current best are pruned (alpha-beta cutoff).

## License

[MIT](LICENSE). Made by Rafael Bachourian.
