# Anggota: Afsal Murtaza | 5025241190
from digit_relay.relay_node import RelayNode, run


class Member4(RelayNode):
    def __init__(self):
        super().__init__('member4')


def main():
    run(Member4)


if __name__ == '__main__':
    main()
