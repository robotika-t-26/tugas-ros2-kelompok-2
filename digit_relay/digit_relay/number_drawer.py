# Menggambar angka (1 atau 2 digit) memakai definisi segmen dari digits.py.

# Anggota : Nabila Shafa Rahayu - 5025241150

# Segmen disusun agar sebisa mungkin tersambung (ujung segmen sebelumnya = awal segmen berikutnya)

from digit_relay.digits import DIGIT_GAP, DIGIT_SEGMENTS, DIGIT_W, segment_points

EPS = 1e-6


def _same(p, q) -> bool:
    return abs(p[0] - q[0]) < EPS and abs(p[1] - q[1]) < EPS


def plan_strokes(digit: int, x: float, y: float, scale: float):
    # Urutkan segmen digit menjadi daftar garis (awal, akhir) yang sebanyak mungkin tersambung. Fungsi murni, bisa dites tanpa ROS.
    remaining = [segment_points(s, x, y, scale) for s in DIGIT_SEGMENTS[digit]]
    strokes = []
    cur = None
    while remaining:
        pick = None
        if cur is not None:
            for i, (p, q) in enumerate(remaining):
                if _same(p, cur):
                    pick = (i, p, q)
                    break
                if _same(q, cur):
                    pick = (i, q, p)
                    break
        if pick is None:
            p, q = remaining[0]
            pick = (0, p, q)
        i, p, q = pick
        remaining.pop(i)
        strokes.append((p, q))
        cur = q
    return strokes


def digit_origins(n: int, x: float, y: float, scale: float):
    # Pasangan (digit, x_digit) untuk setiap digit angka n
    return [
        (int(ch), x + i * (DIGIT_W + DIGIT_GAP) * scale)
        for i, ch in enumerate(str(n))
    ]


def draw_digit(turtle, digit: int, x: float, y: float, scale: float, step: float = 0.05) -> None:
    # Gambar satu digit dengan pojok kiri bawah di (x, y)
    cur = None
    for start, end in plan_strokes(digit, x, y, scale):
        if cur is None or not _same(cur, start):
            turtle.pen_up()
            turtle.teleport(*start)
            turtle.pen_down()
        turtle.line_to(*end, step=step)
        cur = end


def draw_number(turtle, n: int, x: float, y: float, scale: float = 1.0, step: float = 0.05) -> None:
    # Gambar angka n (misalnya 7 atau 12) mulai dari (x, y).
    for digit, dx in digit_origins(n, x, y, scale):
        draw_digit(turtle, digit, dx, y, scale, step)
    turtle.pen_up()
