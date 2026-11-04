"""Node Anggota 3 - Slot 3.

Pemilik: Anggota 3
"""
from digit_relay.relay_node import RelayNode, run


class Member3(RelayNode):
    def __init__(self):
        super().__init__('member3')


def main():
    run(Member3)


if __name__ == '__main__':
    main()
