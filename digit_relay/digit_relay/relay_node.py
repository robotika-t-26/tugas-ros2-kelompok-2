# Anggota: Afsal Murtaza | 5025241190

import threading

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node

from digit_relay.digits import CANVAS_MAX, CANVAS_MIN, slot_bbox
from digit_relay.number_drawer import draw_number
from digit_relay.turtle_utils import TurtleClient
from digit_relay_interfaces.msg import Turn

TURN_TOPIC = '/turn'
DONE_SIGNAL = 0

class RelayNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self.member_id = self.declare_parameter('member_id', 0).value
        self.total_members = self.declare_parameter('total_members', 6).value
        self.max_number = self.declare_parameter('max_number', 12).value
        self.slot_x = self.declare_parameter('slot_x', 0.0).value
        self.slot_y = self.declare_parameter('slot_y', 0.0).value
        self.pen_color = (
            self.declare_parameter('pen_r', 255).value,
            self.declare_parameter('pen_g', 255).value,
            self.declare_parameter('pen_b', 255).value,
        )
        self.pen_width = self.declare_parameter('pen_width', 3).value
        self.scale = self.declare_parameter('scale', 1.0).value
        self.draw_step = self.declare_parameter('draw_step', 0.05).value

        self._check_own_slot()

        self.cb_group = ReentrantCallbackGroup()
        self.turtle = TurtleClient(self, self.cb_group)

        self.turtle.wait_for_services()

        self.turn_pub = self.create_publisher(Turn, TURN_TOPIC, 10)
        self.turn_sub = self.create_subscription(
            Turn, TURN_TOPIC, self.on_turn, 10, callback_group=self.cb_group
        )

        self._lock = threading.Lock()
        self.last_drawn = 0
        self.finished = False

        if self.is_starter():
            self._kickoff_timer = self.create_timer(
                0.5, self.kickoff, callback_group=self.cb_group
            )

        self.get_logger().info(
            f'Anggota {self.member_id} siap di slot ({self.slot_x}, {self.slot_y}), idle'
        )

    def _check_own_slot(self) -> None:
        x1, y1, x2, y2 = slot_bbox(self.slot_x, self.slot_y, self.scale)
        if x1 < CANVAS_MIN or y1 < CANVAS_MIN or x2 > CANVAS_MAX or y2 > CANVAS_MAX:
            self.get_logger().warn('Angka 2 digit di slot ini akan keluar kanvas!')

    def is_starter(self) -> bool:

        return False

    def before_draw(self, number: int) -> None:
        pass

    def after_draw(self, number: int) -> bool:

        return True

    def kickoff(self) -> None:

        subs = self.turn_pub.get_subscription_count()
        if subs < self.total_members:
            self.get_logger().info(f'Menunggu node lain ({subs}/{self.total_members}) ...')
            return
        self._kickoff_timer.cancel()
        self.get_logger().info('Semua node siap, relay dimulai')
        self.turn_pub.publish(Turn(current_number=1, active_member=self.member_id))

    def on_turn(self, msg: Turn) -> None:

        if msg.active_member == DONE_SIGNAL:
            if not self.finished:
                self.finished = True
                self.get_logger().info('Relay selesai, node idle')
            return
        if self.finished:
            return
        if msg.active_member != self.member_id:
            return
        number = msg.current_number
        if number <= self.last_drawn or number > self.max_number:
            return
        if not self._lock.acquire(blocking=False):
            return
        try:
            self.do_turn(number)
        finally:
            self._lock.release()

    def do_turn(self, number: int) -> None:

        self.get_logger().info(f'Giliran Anggota {self.member_id}: menggambar {number}')
        self.before_draw(number)
        r, g, b = self.pen_color
        self.turtle.set_pen(r, g, b, self.pen_width, off=1)
        self.turtle.wait_for_pose()
        draw_number(self.turtle, number, self.slot_x, self.slot_y, self.scale, self.draw_step)
        self.last_drawn = number
        if self.after_draw(number):
            self.pass_turn(number)

    def pass_turn(self, number: int) -> None:

        nxt = self.next_member()
        self.get_logger().info(f'Oper giliran ke Anggota {nxt} (angka {number + 1})')
        self.turn_pub.publish(Turn(current_number=number + 1, active_member=nxt))

    def next_member(self) -> int:
        return self.member_id % self.total_members + 1

def run(node_cls) -> None:

    rclpy.init()
    node = node_cls()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        rclpy.try_shutdown()
