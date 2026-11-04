"""Node Anggota 1 - Slot 1. Memulai siklus pertama dan transisi /clear.

Pemilik: Anggota 1
"""
from digit_relay.relay_node import RelayNode, run
from digit_relay.turtle_utils import transition_to_next_cycle


class Member1(RelayNode):
    def __init__(self):
        super().__init__('member1')

    def is_starter(self) -> bool:
        return True

    def before_draw(self, number: int) -> None:
        # Angka pertama siklus 2 (N+1): bersihkan kanvas dulu
        if number == self.total_members + 1:
            transition_to_next_cycle(self.turtle)


def main():
    run(Member1)


if __name__ == '__main__':
    main()
