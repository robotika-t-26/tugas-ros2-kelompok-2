# Node Anggota 2 - Slot 2.

# Anggota: Via Hana Nurma Putri - 5025241048

from digit_relay.relay_node import RelayNode, run


class Member2(RelayNode):
    def __init__(self):
        super().__init__('member2')


def main():
    run(Member2)


if __name__ == '__main__':
    main()
