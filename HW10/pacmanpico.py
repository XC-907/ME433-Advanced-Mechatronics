import pgzrun
import math
import random
import pygame

import serial

import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
 
WIDTH  = 560
HEIGHT = 660
TITLE  = "Pac-Man Zero"
 
CELL = 28
COLS = 20
ROWS = 20
 
RAW_MAZE = [
    "11111111111111111111",
    "10000000011000000001",
    "13111011101101101131",
    "10000000000000000001",
    "10111011111110110101",
    "10000010000010000001",
    "11101011010110101101",
    "22101000010000101022",
    "11101011111110101101",
    "10000010222210000001",
    "10111010111110110001",
    "10000000000000000001",
    "10111011010110111101",
    "13001010000010101031",
    "11101010111110101101",
    "10000000011000000001",
    "10111111101101111101",
    "10000000000000000001",
    "11011011111110110111",
    "10000000011000000001",
]
 
BASE_MAZE = [[int(ch) for ch in row] for row in RAW_MAZE]
 
DIRS = {
    "left":  (-1,  0),
    "right": ( 1,  0),
    "up":    ( 0, -1),
    "down":  ( 0,  1),
}
 
GHOST_COLORS = [
    (255,  50,  80),
    (  0, 220, 255),
    (255, 140,   0),
    (255, 100, 200),
]
 
# ---- sound ------------------------------------------------------------------
# pgzero auto-loads from the sounds/ folder next to this script.
# Just call sounds.burp.play() directly.
 
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
 
# ---- helpers ----------------------------------------------------------------
 
def fresh_dots():
    return [[int(ch) for ch in row] for row in RAW_MAZE]
 
def walkable(dots, col, row):
    if col < 0 or col >= COLS or row < 0 or row >= ROWS:
        return False
    return dots[row][col] != 1
 
def count_dots(dots):
    return sum(1 for row in dots for c in row if c in (0, 3))
 

ser = serial.Serial('COM9')        # My COM port
print('Opening port: ' + str(ser.name))
 
TILT_THRESHOLD = 0.1
 
# ---- input function ---------------------------------------------------------
# Reads ax, ay from Pico over serial and returns a direction string.
 
def get_player_input():

    # Keep previous player input code
    if keyboard.left:  return "left"
    if keyboard.right: return "right"
    if keyboard.up:    return "up"
    if keyboard.down:  return "down"

     # Drain buffer, only keep the latest line
    latest = None
    while ser.in_waiting:
        latest = ser.readline()
    if latest is None:
        latest = ser.readline()

    s = str(latest)
    result1 = s[s.find('(')+1:s.find(',')]
    result2 = s[s.find(',')+1:s.find(')')]

    if result1 == '' or result2 == '':
        return None

    ax = float(result1)
    ay = float(result2)

    if abs(ax) > abs(ay):
        if ax >  TILT_THRESHOLD: return "left"
        elif ax < -TILT_THRESHOLD: return "right"
    else:
        if ay >  TILT_THRESHOLD: return "down"
        elif ay < -TILT_THRESHOLD: return "up"

    return None
 
# ---- player -----------------------------------------------------------------
 
class Player:
    START_COL = 10
    START_ROW = 13
    SPEED = 2
 
    def __init__(self):
        self.reset()
 
    def reset(self):
        self.col = self.START_COL
        self.row = self.START_ROW
        self.px  = self.col * CELL + CELL // 2
        self.py  = self.row * CELL + CELL // 2 + 40
        self.dir      = DIRS["right"]
        self.next_dir = DIRS["right"]
        self.mouth       = 0
        self.mouth_open  = True
 
    def cell_center(self):
        return (self.col * CELL + CELL // 2,
                self.row * CELL + CELL // 2 + 40)
 
    def update(self, dots, desired):
        if desired:
            self.next_dir = DIRS[desired]
 
        tx, ty = self.cell_center()
        dx, dy = tx - self.px, ty - self.py
 
        if abs(dx) <= self.SPEED and abs(dy) <= self.SPEED:
            self.px, self.py = tx, ty
            dc, dr = self.next_dir
            if walkable(dots, self.col + dc, self.row + dr):
                self.dir = self.next_dir
                self.col += dc
                self.row += dr
            else:
                cc, cr = self.dir
                if walkable(dots, self.col + cc, self.row + cr):
                    self.col += cc
                    self.row += cr
        else:
            if abs(dx): self.px += self.SPEED if dx > 0 else -self.SPEED
            if abs(dy): self.py += self.SPEED if dy > 0 else -self.SPEED
 
        step = 5
        if self.mouth_open:
            self.mouth = min(self.mouth + step, 35)
            if self.mouth >= 35: self.mouth_open = False
        else:
            self.mouth = max(self.mouth - step, 2)
            if self.mouth <= 2:  self.mouth_open = True
 
    def draw(self):
        d = self.dir
        if   d == DIRS["right"]: angle = 0
        elif d == DIRS["left"]:  angle = 180
        elif d == DIRS["up"]:    angle = 270
        else:                    angle = 90
 
        r  = CELL // 2 - 2
        cx, cy = self.px, self.py
 
        # Draw full yellow circle
        screen.draw.filled_circle((cx, cy), r, (255, 220, 0))
 
        # Cut mouth out with a black triangle - both points use -sin (pygame Y flipped)
        a = math.radians(angle)
        m = math.radians(self.mouth)
        p1 = (int(cx + r * math.cos(a + m)), int(cy - r * math.sin(a + m)))
        p2 = (int(cx + r * math.cos(a - m)), int(cy - r * math.sin(a - m)))
        pygame.draw.polygon(screen.surface, (0, 0, 0), [(cx, cy), p1, p2])
 
        # Eye always sits above centre
        screen.draw.filled_circle((cx, cy - r // 2), 2, (0, 0, 0))
 
 
# ---- ghost ------------------------------------------------------------------
 
class Ghost:
    STARTS = [(9, 9), (10, 9), (11, 9), (10, 8)]
    SPEED  = 1
 
    def __init__(self, idx):
        self.idx   = idx
        self.color = GHOST_COLORS[idx]
        self.reset()
 
    def reset(self):
        self.col, self.row = self.STARTS[self.idx]
        self.px = self.col * CELL + CELL // 2
        self.py = self.row * CELL + CELL // 2 + 40
        self.dir    = random.choice(list(DIRS.values()))
        self.scared = False
        self.scared_timer = 0
 
    def cell_center(self):
        return (self.col * CELL + CELL // 2,
                self.row * CELL + CELL // 2 + 40)
 
    def update(self, dots, pcol, prow):
        if self.scared_timer > 0:
            self.scared_timer -= 1
            if self.scared_timer == 0:
                self.scared = False
 
        tx, ty = self.cell_center()
        dx, dy = tx - self.px, ty - self.py
 
        if abs(dx) <= self.SPEED and abs(dy) <= self.SPEED:
            self.px, self.py = tx, ty
            self._pick_dir(dots, pcol, prow)
            dc, dr = self.dir
            self.col += dc
            self.row += dr
        else:
            if abs(dx): self.px += self.SPEED if dx > 0 else -self.SPEED
            if abs(dy): self.py += self.SPEED if dy > 0 else -self.SPEED
 
    def _pick_dir(self, dots, pcol, prow):
        rev  = (-self.dir[0], -self.dir[1])
        opts = [d for d in DIRS.values()
                if d != rev and walkable(dots, self.col + d[0], self.row + d[1])]
        if not opts and walkable(dots, self.col + rev[0], self.row + rev[1]):
            opts = [rev]
        if not opts:
            return
        if self.scared or random.random() < 0.25:
            self.dir = random.choice(opts)
        else:
            self.dir = min(opts, key=lambda d: (
                abs(self.col + d[0] - pcol) + abs(self.row + d[1] - prow)))
 
    def draw(self):
        r  = CELL // 2 - 2
        cx, cy = self.px, self.py
        col = (80, 80, 255) if self.scared else self.color
 
        screen.draw.filled_circle((cx, cy - r // 2), r, col)
        screen.draw.filled_rect(
            pygame.Rect(cx - r, cy - r // 2, r * 2, r + r // 2), col)
        for i in range(3):
            bx = cx - r + i * r + r // 3
            screen.draw.filled_circle((bx, cy + r // 2), r // 3, (0, 0, 0))
        for ex_off in (-r // 3, r // 3):
            screen.draw.filled_circle((cx + ex_off, cy - r // 3), r // 4, (255, 255, 255))
            pupil = (0, 0, 180) if not self.scared else (255, 0, 0)
            screen.draw.filled_circle((cx + ex_off + 1, cy - r // 3 + 1), r // 6, pupil)
 
 
# ---- game state -------------------------------------------------------------
 
def new_game():
    return dict(
        dots      = fresh_dots(),
        dot_count = count_dots(fresh_dots()),
        score     = 0,
        lives     = 3,
        player    = Player(),
        ghosts    = [Ghost(i) for i in range(4)],
        state     = "playing",
    )
 
def reset_round(g):
    g["player"].reset()
    for gh in g["ghosts"]:
        gh.reset()
    g["state"] = "playing"
 
game = new_game()
 
# ---- pgzero callbacks -------------------------------------------------------
 
def update():
    global game
    if keyboard.space and game["state"] in ("dead", "won"):
        game = new_game()
        return
 
    if game["state"] != "playing":
        return
 
    desired = get_player_input()
    g = game
 
    g["player"].update(g["dots"], desired)
    for gh in g["ghosts"]:
        gh.update(g["dots"], g["player"].col, g["player"].row)
 
    pc, pr = g["player"].col, g["player"].row
    cell = g["dots"][pr][pc]
    if cell == 0:
        g["dots"][pr][pc] = 2
        g["score"] += 10
        g["dot_count"] -= 1
    elif cell == 3:
        g["dots"][pr][pc] = 2
        g["score"] += 50
        g["dot_count"] -= 1
        for gh in g["ghosts"]:
            gh.scared = True
            gh.scared_timer = 120
 
    for gh in g["ghosts"]:
        if (abs(gh.px - g["player"].px) < CELL - 6 and
                abs(gh.py - g["player"].py) < CELL - 6):
            if gh.scared:
                gh.reset()
                g["score"] += 200
            else:
                g["lives"] -= 1
                sounds.burp.play()
                if g["lives"] <= 0:
                    g["state"] = "dead"
                else:
                    reset_round(g)
            break
 
    if g["dot_count"] <= 0:
        g["state"] = "won"
 
 
def draw():
    g = game
    screen.fill((0, 0, 0))
 
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL
            y = r * CELL + 40
            base = BASE_MAZE[r][c]
            dot  = g["dots"][r][c]
            if base == 1:
                screen.draw.filled_rect(pygame.Rect(x, y, CELL, CELL), (10, 20, 120))
                screen.draw.rect(pygame.Rect(x + 1, y + 1, CELL - 2, CELL - 2), (30, 60, 200))
            elif dot == 0:
                screen.draw.filled_circle((x + CELL // 2, y + CELL // 2), 3, (220, 190, 140))
            elif dot == 3:
                pulse = int(5 + 3 * math.sin(pygame.time.get_ticks() / 150))
                screen.draw.filled_circle((x + CELL // 2, y + CELL // 2), pulse, (255, 255, 160))
 
    if g["state"] == "playing":
        g["player"].draw()
        for gh in g["ghosts"]:
            gh.draw()
 
    screen.draw.text("SCORE: " + str(g["score"]), (10, 10),
                     color=(255, 220, 0), fontsize=22)
    for i in range(g["lives"]):
        lx = WIDTH - 20 - i * 22
        screen.draw.filled_circle((lx, 20), 8, (255, 220, 0))
 
    if g["state"] == "dead":
        screen.draw.filled_rect(pygame.Rect(70, 220, WIDTH - 140, 120), (0, 0, 30))
        screen.draw.rect(pygame.Rect(70, 220, WIDTH - 140, 120), (255, 220, 0))
        screen.draw.text("GAME OVER", center=(WIDTH // 2, 255),
                         color=(255, 220, 0), fontsize=40)
        screen.draw.text("Score: " + str(g["score"]) + "  -  SPACE to restart",
                         center=(WIDTH // 2, 305), color=(200, 200, 200), fontsize=18)
 
    elif g["state"] == "won":
        screen.draw.filled_rect(pygame.Rect(70, 220, WIDTH - 140, 120), (0, 0, 30))
        screen.draw.rect(pygame.Rect(70, 220, WIDTH - 140, 120), (255, 220, 0))
        screen.draw.text("YOU WIN!", center=(WIDTH // 2, 255),
                         color=(255, 220, 0), fontsize=40)
        screen.draw.text("Score: " + str(g["score"]) + "  -  SPACE to restart",
                         center=(WIDTH // 2, 305), color=(200, 200, 200), fontsize=18)
 
 
pgzrun.go()
 