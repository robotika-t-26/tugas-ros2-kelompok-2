"""Logika terminasi setelah siklus kedua selesai.

Pemilik: Anggota 6

Cara kerja:
  1. Setelah angka terakhir (2N) digambar, node terakhir tidak mengoper giliran,
     melainkan mengirim pesan Turn dengan active_member = DONE_SIGNAL (0).
  2. Semua node (termasuk pengirim) menerima sinyal itu lalu masuk state idle:
     tidak ada lagi giliran yang diproses.
"""
from digit_relay_interfaces.msg import Turn

DONE_SIGNAL = 0


def is_last_number(number: int, max_number: int) -> bool:
    """True jika angka yang baru digambar adalah angka terakhir (2N)."""
    return number >= max_number


def finish_relay(node) -> None:
    """Kirim sinyal selesai ke semua node."""
    node.get_logger().info('Angka terakhir selesai digambar, mengirim sinyal selesai')
    node.turn_pub.publish(Turn(current_number=node.max_number, active_member=DONE_SIGNAL))
