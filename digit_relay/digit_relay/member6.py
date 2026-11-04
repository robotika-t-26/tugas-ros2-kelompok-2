"""Node Anggota 6 - Slot 6.

Pemilik: Adriel Mahira Dharma - 5025241097
"""
from digit_relay.relay_node import RelayNode, run
from digit_relay.termination import finish_relay, is_last_number


class Member6(RelayNode):
    def __init__(self):
        super().__init__('member6')

    def after_draw(self, number: int) -> bool:
        if is_last_number(number, self.max_number):
            finish_relay(self)
            return False   # jangan oper giliran lagi
        return True


def main():
    run(Member6)


if __name__ == '__main__':
    main()
