"""Definisi digit 0-9 gaya 7-segmen dan aturan layout slot.

Pemilik: Anggota 3

Konvensi:
  - Satu digit berukuran DIGIT_W x DIGIT_H (dikali scale).
  - Titik acuan (x, y) adalah pojok KIRI BAWAH digit.
  - Segmen dinamai seperti display 7-segmen:

         aaa
        f   b
         ggg
        e   c
         ddd
"""

# Ukuran dasar satu digit (sebelum dikali scale)
DIGIT_W = 1.0
DIGIT_H = 2.0
# Jarak antardigit pada angka 2 digit (sebelum dikali scale)
DIGIT_GAP = 0.5

# Batas kanvas aman (turtlesim kira-kira 0.0 - 11.08)
CANVAS_MIN = 0.5
CANVAS_MAX = 10.5

# Titik ujung tiap segmen, relatif terhadap pojok kiri bawah.
# x dikali DIGIT_W, y dikali DIGIT_H.
SEGMENT_LINES = {
    'a': ((0.0, 1.0), (1.0, 1.0)),
    'b': ((1.0, 1.0), (1.0, 0.5)),
    'c': ((1.0, 0.5), (1.0, 0.0)),
    'd': ((0.0, 0.0), (1.0, 0.0)),
    'e': ((0.0, 0.5), (0.0, 0.0)),
    'f': ((0.0, 1.0), (0.0, 0.5)),
    'g': ((0.0, 0.5), (1.0, 0.5)),
}

# Segmen yang menyala untuk tiap digit.
DIGIT_SEGMENTS = {
    0: 'abcdef',
    1: 'bc',
    2: 'abged',
    3: 'abgcd',
    4: 'fgbc',
    5: 'afgcd',
    6: 'afgedc',
    7: 'abc',
    8: 'abcdefg',
    9: 'abcdfg',
}


def segment_points(segment: str, x: float, y: float, scale: float):
    """Koordinat absolut (awal, akhir) satu segmen untuk digit di (x, y)."""
    (ux1, uy1), (ux2, uy2) = SEGMENT_LINES[segment]
    w, h = DIGIT_W * scale, DIGIT_H * scale
    return (x + ux1 * w, y + uy1 * h), (x + ux2 * w, y + uy2 * h)


def number_width(n_digits: int, scale: float) -> float:
    """Lebar total angka dengan n_digits digit."""
    return (n_digits * DIGIT_W + (n_digits - 1) * DIGIT_GAP) * scale


def slot_bbox(x: float, y: float, scale: float, n_digits: int = 2):
    """Bounding box (xmin, ymin, xmax, ymax) angka di slot (x, y)."""
    return (x, y, x + number_width(n_digits, scale), y + DIGIT_H * scale)


def check_layout(slots, scale: float, canvas_min: float = CANVAS_MIN,
                 canvas_max: float = CANVAS_MAX) -> bool:
    """Cek bahwa angka 2 digit di setiap slot tidak keluar kanvas dan tidak overlap.

    slots: daftar (x, y) pojok kiri bawah tiap slot.
    """
    boxes = [slot_bbox(x, y, scale) for x, y in slots]
    for (x1, y1, x2, y2) in boxes:
        if x1 < canvas_min or y1 < canvas_min or x2 > canvas_max or y2 > canvas_max:
            return False
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            overlap = a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
            if overlap:
                return False
    return True


# Layout yang dipakai di config/members.yaml (2 baris x 3 kolom)
DEFAULT_SLOTS = [(1.0, 7.0), (4.5, 7.0), (8.0, 7.0), (1.0, 2.0), (4.5, 2.0), (8.0, 2.0)]


if __name__ == '__main__':
    print('Layout valid:', check_layout(DEFAULT_SLOTS, scale=1.0))
