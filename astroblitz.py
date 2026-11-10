# ASTRO BLITZ - jeu de tir spatial pour NumWorks
# Fleches : bouger | OK ou EXE : tirer | Retour : quitter
from kandinsky import fill_rect, draw_string
from ion import keydown, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_OK, KEY_EXE, KEY_BACK
from time import sleep, monotonic
from random import randint, random

W, H, TOP = 320, 222, 18
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
CYAN = (0, 220, 255)
JAUNE = (255, 220, 0)
ROUGE = (255, 50, 50)
VERT = (60, 255, 100)
ROSE = (255, 80, 200)
ORANGE = (255, 140, 0)
GRIS = (90, 90, 90)
HUD = (20, 20, 60)

record = 0


def ship(x, y, c):
    fill_rect(x + 6, y, 3, 4, c)
    fill_rect(x + 3, y + 4, 9, 4, c)
    fill_rect(x, y + 7, 15, 3, c)
    fill_rect(x + 6, y + 10, 3, 2, ORANGE if c != NOIR else NOIR)


def enemy(e, c):
    x, y, t = int(e[0]), int(e[1]), e[2]
    if t == 0:  # rodeur
        fill_rect(x, y, 12, 4, c)
        fill_rect(x + 2, y + 4, 8, 4, c)
        if c != NOIR:
            fill_rect(x + 3, y + 1, 2, 2, NOIR)
            fill_rect(x + 7, y + 1, 2, 2, NOIR)
    elif t == 1:  # zigzag
        fill_rect(x + 4, y, 4, 12, c)
        fill_rect(x, y + 4, 12, 4, c)
    else:  # tank (2 PV)
        fill_rect(x, y, 16, 12, c)
        if c != NOIR:
            fill_rect(x + 3, y + 3, 10, 6, GRIS if e[4] > 1 else ROUGE)


ECOL = (ROUGE, ROSE, VERT)
ESIZE = ((12, 8), (12, 12), (16, 12))


def bonus(b, c):
    x, y = int(b[0]), int(b[1])
    fill_rect(x, y, 10, 10, c)
    if c != NOIR:
        if b[2] == 0:  # triple tir
            fill_rect(x + 4, y + 1, 2, 8, NOIR)
            fill_rect(x + 1, y + 4, 8, 2, NOIR)
        else:  # vie
            fill_rect(x + 2, y + 2, 2, 2, NOIR)
            fill_rect(x + 6, y + 2, 2, 2, NOIR)
            fill_rect(x + 3, y + 6, 4, 2, NOIR)


BCOL = (ROSE, ORANGE, ROUGE, VERT)


def boss_draw(bo, niv, flash):
    x, y = int(bo[0]), int(bo[1])
    c = BLANC if flash else BCOL[(niv - 1) % 4]
    fill_rect(x + 4, y, 32, 14, c)
    fill_rect(x, y + 6, 40, 6, c)
    fill_rect(x + 6, y + 14, 4, 8, c)
    fill_rect(x + 30, y + 14, 4, 8, c)
    fill_rect(x + 17, y + 14, 6, 6, c)
    fill_rect(x + 12, y + 4, 5, 4, NOIR)
    fill_rect(x + 23, y + 4, 5, 4, NOIR)


def message(txt, col):
    x = 160 - len(txt) * 5
    draw_string(txt, x, 100, col, NOIR)
    sleep(1.2)
    fill_rect(x, 100, len(txt) * 10, 18, NOIR)


def hud(score, vies, niv, triple, bo=None):
    fill_rect(0, 0, W, TOP, HUD)
    draw_string("SCORE " + str(score), 4, 1, BLANC, HUD)
    if bo:
        fill_rect(120, 5, 92, 8, GRIS)
        fill_rect(120, 5, 92 * bo[2] // bo[3], 8, ROUGE)
    else:
        draw_string("NIV " + str(niv), 140, 1, JAUNE, HUD)
    for i in range(vies):
        fill_rect(250 + i * 14, 5, 10, 8, ROUGE)
    if triple > 0:
        draw_string("x3", 222, 1, CYAN, HUD)


def wait_key():
    while keydown(KEY_OK) or keydown(KEY_EXE):
        sleep(0.02)
    while True:
        if keydown(KEY_OK) or keydown(KEY_EXE):
            return True
        if keydown(KEY_BACK):
            return False
        sleep(0.02)


def title():
    fill_rect(0, 0, W, H, NOIR)
    for _ in range(40):
        fill_rect(randint(0, W - 1), randint(0, H - 1), 1, 1, BLANC)
    draw_string("A S T R O   B L I T Z", 55, 40, CYAN, NOIR)
    ship(152, 75, CYAN)
    draw_string("Fleches : bouger", 80, 110, BLANC, NOIR)
    draw_string("OK / EXE : tirer", 80, 130, BLANC, NOIR)
    draw_string("+ = triple tir   coeur = vie", 20, 145, JAUNE, NOIR)
    draw_string("Un BOSS tous les 200 pts !", 30, 160, ROUGE, NOIR)
    draw_string("Record : " + str(record), 100, 178, VERT, NOIR)
    draw_string("OK pour jouer", 95, 198, ORANGE, NOIR)
    return wait_key()


def hit(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def play():
    fill_rect(0, 0, W, H, NOIR)
    px, py = 152.0, 196.0
    shots, enemies, bonuses = [], [], []
    stars = [[randint(0, W - 1), randint(TOP, H - 1), randint(1, 3)] for _ in range(18)]
    score, vies, niv = 0, 3, 1
    cool, triple, invul, spawn = 0, 0, 0, 0.0
    hud(score, vies, niv, triple)
    dirty = False
    last = -1
    bo = None  # boss : [x, y, pv, pv_max, direction, recharge]
    bshots = []
    seuil = 200
    flash = 0
    while True:
        t0 = monotonic()
        if keydown(KEY_BACK):
            return score
        # --- effacer ---
        ship(int(px), int(py), NOIR)
        for s in shots:
            fill_rect(int(s[0]), int(s[1]), 2, 6, NOIR)
        for e in enemies:
            enemy(e, NOIR)
        for b in bonuses:
            bonus(b, NOIR)
        for st in stars:
            fill_rect(st[0], st[1], 1, 1, NOIR)
        if bo:
            fill_rect(int(bo[0]), int(bo[1]), 40, 22, NOIR)
        for s in bshots:
            fill_rect(int(s[0]), int(s[1]), 4, 4, NOIR)
        # --- joueur ---
        if keydown(KEY_LEFT):
            px -= 5
        if keydown(KEY_RIGHT):
            px += 5
        if keydown(KEY_UP):
            py -= 4
        if keydown(KEY_DOWN):
            py += 4
        px = max(0, min(W - 15, px))
        py = max(TOP + 60, min(H - 13, py))
        if cool > 0:
            cool -= 1
        if (keydown(KEY_OK) or keydown(KEY_EXE)) and cool == 0:
            shots.append([px + 6, py - 6, 0])
            if triple > 0:
                shots.append([px + 1, py, -1.5])
                shots.append([px + 12, py, 1.5])
            cool = 5
        if triple > 0:
            triple -= 1
            if triple == 0:
                dirty = True
        if invul > 0:
            invul -= 1
        # --- tirs ---
        for s in shots:
            s[1] -= 7
            s[0] += s[2]
        shots = [s for s in shots if s[1] > TOP and 0 < s[0] < W - 2]
        # --- ennemis ---
        if bo is None and score >= seuil:
            bo = [140.0, float(TOP + 1), 25 + niv * 15, 25 + niv * 15, 1, 40]
            message("ALERTE : BOSS !", ROUGE)
            dirty = True
        if bo is None:
            spawn += 0.03 + niv * 0.012
        if spawn >= 1:
            spawn -= 1
            r = random()
            t = 0 if r < 0.6 else (1 if r < 0.85 or niv < 2 else 2)
            ew = ESIZE[t][0]
            sp = 1.0 + niv * 0.25 + random()
            if t == 2:
                sp *= 0.6
            enemies.append([float(randint(0, W - ew)), float(TOP + 1), t, sp, 2 if t == 2 else 1, random() * 6])
        alive = []
        for e in enemies:
            e[1] += e[3]
            if e[2] == 1:
                e[5] += 0.15
                e[0] += 2.5 if int(e[5]) % 2 == 0 else -2.5
                e[0] = max(0, min(W - 12, e[0]))
            ew, eh = ESIZE[e[2]]
            dead = False
            for s in shots:
                if hit(s[0], s[1], 2, 6, e[0], e[1], ew, eh):
                    s[1] = -99
                    e[4] -= 1
                    if e[4] <= 0:
                        dead = True
                        score += (10, 15, 30)[e[2]]
                        if random() < 0.08:
                            bonuses.append([e[0], e[1], 0 if random() < 0.7 else 1])
                    break
            if dead:
                continue
            if invul == 0 and hit(px, py, 15, 12, e[0], e[1], ew, eh):
                vies -= 1
                invul = 45
                dirty = True
                continue
            if e[1] > H - eh:
                score = max(0, score - 5)
                dirty = True
                continue
            alive.append(e)
        enemies = alive
        shots = [s for s in shots if s[1] > 0]
        # --- boss ---
        if flash > 0:
            flash -= 1
        if bo:
            if bo[1] < TOP + 12:
                bo[1] += 0.5
            bo[0] += bo[4] * (1 + niv * 0.4)
            if bo[0] < 0 or bo[0] > W - 40:
                bo[4] = -bo[4]
                bo[0] = max(0, min(W - 40, bo[0]))
            bo[5] -= 1
            if bo[5] <= 0:
                bo[5] = max(14, 45 - niv * 5)
                cx, cy = bo[0] + 18, bo[1] + 20
                dx = (px + 7 - cx) / 60
                dx = max(-2.5, min(2.5, dx))
                bshots.append([cx, cy, dx, 3.0])
                if niv >= 2:
                    bshots.append([cx - 12, cy, dx - 1.2, 3.0])
                    bshots.append([cx + 12, cy, dx + 1.2, 3.0])
                if niv >= 3:
                    bshots.append([cx, cy, dx, 4.5])
            for s in shots:
                if hit(s[0], s[1], 2, 6, bo[0], bo[1], 40, 22):
                    s[1] = -99
                    bo[2] -= 1
                    flash = 2
                    dirty = True
            shots = [s for s in shots if s[1] > 0]
            if bo[2] <= 0:
                bx, by = int(bo[0]), int(bo[1])
                for i in range(6):
                    fill_rect(bx, by, 40, 22, JAUNE if i % 2 == 0 else ORANGE)
                    sleep(0.08)
                fill_rect(bx, by, 40, 22, NOIR)
                for s in bshots:
                    fill_rect(int(s[0]), int(s[1]), 4, 4, NOIR)
                bshots = []
                score += 100 * niv
                bonuses.append([bo[0] + 5.0, bo[1], 0])
                bonuses.append([bo[0] + 25.0, bo[1], 1])
                bo = None
                niv += 1
                seuil = score + 200 + niv * 50
                message("BOSS VAINCU ! NIVEAU " + str(niv), JAUNE)
                dirty = True
        keepb = []
        for s in bshots:
            s[0] += s[2]
            s[1] += s[3]
            if invul == 0 and hit(px, py, 15, 12, s[0], s[1], 4, 4):
                vies -= 1
                invul = 45
                dirty = True
            elif s[1] < H - 4 and 0 < s[0] < W - 4:
                keepb.append(s)
        bshots = keepb
        # --- bonus ---
        keep = []
        for b in bonuses:
            b[1] += 1.5
            if hit(px, py, 15, 12, b[0], b[1], 10, 10):
                if b[2] == 0:
                    triple = 300
                elif vies < 5:
                    vies += 1
                score += 20
                dirty = True
            elif b[1] < H - 10:
                keep.append(b)
        bonuses = keep
        # --- niveau / HUD ---
        if dirty or score != last:
            hud(score, vies, niv, triple, bo)
            last = score
            dirty = False
        if vies <= 0:
            return score
        # --- dessiner ---
        for st in stars:
            st[1] += st[2]
            if st[1] >= H:
                st[1] = TOP
                st[0] = randint(0, W - 1)
            fill_rect(st[0], st[1], 1, 1, GRIS if st[2] < 3 else BLANC)
        for b in bonuses:
            bonus(b, CYAN if b[2] == 0 else ROUGE)
        for e in enemies:
            enemy(e, ECOL[e[2]])
        for s in shots:
            fill_rect(int(s[0]), int(s[1]), 2, 6, JAUNE)
        if bo:
            boss_draw(bo, niv, flash > 0)
        for s in bshots:
            fill_rect(int(s[0]), int(s[1]), 4, 4, ORANGE)
        if invul == 0 or invul % 6 < 3:
            ship(int(px), int(py), CYAN)
        dt = 0.033 - (monotonic() - t0)
        if dt > 0:
            sleep(dt)


def game_over(score):
    global record
    nouveau = score > record
    if nouveau:
        record = score
    fill_rect(60, 70, 200, 90, HUD)
    draw_string("GAME OVER", 115, 80, ROUGE, HUD)
    draw_string("Score : " + str(score), 100, 105, BLANC, HUD)
    if nouveau:
        draw_string("NOUVEAU RECORD !", 80, 125, JAUNE, HUD)
    draw_string("OK : rejouer", 100, 142, VERT, HUD)
    return wait_key()


while title():
    if not game_over(play()):
        break
fill_rect(0, 0, W, H, NOIR)
draw_string("A plus dans l'espace !", 50, 100, CYAN, NOIR)
