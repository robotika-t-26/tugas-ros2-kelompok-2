# Node Anggota 5 - Slot 5.

# Anggota : Nabila Shafa Rahayu - 5025241150

from digit_relay.relay_node import RelayNode, run


class Member5(RelayNode):
    def __init__(self):
        super().__init__('member5')


def main():
    run(Member5)


if __name__ == '__main__':
    main()
