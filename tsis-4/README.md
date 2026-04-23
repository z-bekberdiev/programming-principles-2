# TSIS 4: Snake — Database Integration & Advanced Gameplay

## 1. Objective

The goal is to extend the "Snake" game from Practice 10-11 by connecting it to a "PostgreSQL" database for persistent leaderboards, introducing new food behaviors, power-ups, in-game obstacles and polished game screens — all using only PyGame and psycopg2.

---

## 2. Base

| Done In       | Feature                                       |
|:-------------:|-----------------------------------------------|
| `Practice 10` | Wall / border collision detection             |
| `Practice 10` | Random food placement (avoids walls and body) |
| `Practice 10` | Level progression (every N food items)        |
| `Practice 10` | Speed increase per level                      |
| `Practice 10` | Score and level display                       |
| `Practice 11` | Food with different point weights             |
| `Practice 11` | Food that disappears after a timer            |

---

## 3. Tasks

### 3.1. Leaderboard

Integrate the game with a "PostgreSQL" database to persist player results:

1. **Username entry** — on the main menu screen, prompt the player to enter a username (typed via keyboard in PyGame).
2. **Save result** — after game over, automatically save `username`, `score`, `level_reached` and `timestamp` to the database.
3. **Leaderboard screen** — fetch and display the top 10 all-time scores inside the game window.
4. **Personal best** — fetch the player's best score at game start and display it during gameplay.

---

### 3.2. Poison Food

Add a **poison food** item (distinct color, e.g. dark red) as a new food behavior on top of the existing weighted/disappearing foods from Practice 11:

- Appears randomly on the field alongside normal food.
- If the snake eats it: **shorten the snake by 2 segments**.
- If the snake's length drops to 1 or less after eating poison: **game over**.

---

### 3.3. Power-Ups

Spawn temporary power-up items on the field:

| Power-Up    | Effect                                       | Duration        |
|-------------|----------------------------------------------|-----------------|
| Speed boost | Increases snake speed                        | 5 seconds       |
| Slow motion | Decreases snake speed                        | 5 seconds       |
| Shield      | Ignores the next wall or self-collision once | Until triggered |

Rules:
- Only one power-up active on the field at a time.
- Each power-up disappears from the field after **8 seconds** if not collected.
- Use `pygame.time.get_ticks()` to track durations.

---

### 3.4. Obstacles

Starting from **Level 3**, static wall blocks appear inside the arena:

1. Randomly place a set of wall blocks at each new level.
2. Guarantee that the blocks do not surround or trap the snake's current position at spawn time.
3. Collision with an obstacle block → **game over** (same as border collision).
4. Food and power-ups must not spawn on obstacle blocks.

---

### 3.5. Settings (JSON file)

Save and load user preferences from a local `settings.json` file using Python's built-in `json` module:

| Settings     | Options       |
|--------------|---------------|
| Snake color  | Any RGB value |
| Grid overlay | On / Off      |
| Sound        | On / Off      |

Settings are loaded on startup and saved when the user changes them in the `Settings` screen.

---

### 3.6. Game Screens

Implement the following screens using PyGame (no external UI libraries):

1. **Main menu** — buttons: `Play`, `Leaderboard`, `Settings`, `Quit`.
2. **Game over screen** — shows final score, level reached, personal best; buttons: `Retry`, `Main Menu`.
3. **Leaderboard screen** — table with rank, username, score, level, date; button: `Back`.
4. **Settings screen** — toggle grid, toggle sound, pick snake color; button: `Save and Back`.

---

### 3.7. Save to GitHub

Example repository structure:

```
tsis-4/
├── game.py
├── db.py
├── config.py
└── assets/
    ├── settings.json
    └── (room for used sounds)
```
