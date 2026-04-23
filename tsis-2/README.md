# TSIS 2: Paint — Extended Drawing Experience

## 1. Objective

The goal is to extend the "Paint" application from Practice 10-11 by adding freehand drawing, line tools, adjustable brush size, a flood-fill tool, text placement and canvas saving. The focus is on building a more complete drawing experience using only PyGame's built-in capabilities.

---

## 2. Base

| Done In       | Feature                                               |
|:-------------:|-------------------------------------------------------|
| `Practice 10` | Rectangle, circle, eraser, color picker               |
| `Practice 11` | Square, right / equilateral triangle, rhombus         |

---

## 3. Tasks

### 3.1. Freehand & Line Tools

1. **Pencil tool** — while the mouse button is held down, draw continuously along the cursor path using `pygame.draw.line` between consecutive mouse positions.
2. **Straight line tool** — click to set the start point, drag to the end point, release to draw. Show a live preview while dragging.

---

### 3.2. Brush Size

1. Add **three stroke thickness levels**: small (2 px), medium (5 px), large (10 px).
2. Allow switching between sizes via keyboard shortcuts (e.g. `1`, `2`, `3`) or on-screen buttons in the toolbar.
3. Brush size must apply to: pencil, line, rectangle, circle, and all shapes from Practice 10–11.

---

### 3.3. Fill Tool

Implement a **flood fill** tool:

1. The user clicks inside a closed region; the tool fills the area with the currently selected color.
2. Implement using over the canvas pixels via `pygame.Surface.get_at()` and `pygame.Surface.set_at()`.
3. The fill must stop at boundaries of a different color (exact color match is sufficient).

---

### 3.4. Save Canvas

1. Press `Ctrl+S` to save the current canvas as a `PNG` file.
2. Use `pygame.image.save(surface, filename)` — no extra libraries needed.
3. File name should include a timestamp (use Python's `datetime` module) so saves do not overwrite each other.

---

### 3.5. Text Tool

1. The user clicks on the canvas to place a text cursor.
2. Typed characters appear at that position in real time.
3. Press `Enter` to confirm and render the text permanently onto the canvas.
4. Press `Escape` to cancel.
5. Use `pygame.font.SysFont` or `pygame.font.Font` (built-in, no extra libraries).

---

### 3.6. Save to GitHub

Example repository structure:

```
tsis-2/
├── README.md
├── paint.py
└── assets/
    ├── tools.py
    └── images/
        └── (room for used icons and saved canvas)
```
