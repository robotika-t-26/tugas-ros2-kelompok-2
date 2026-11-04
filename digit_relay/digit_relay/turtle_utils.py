# Anggota: Via Hana Nurma Putri - 5025241048

import math
import threading
import time

from rclpy.callback_groups import CallbackGroup
from rclpy.node import Node
from std_srvs.srv import Empty
from turtlesim.msg import Pose
from turtlesim.srv import SetPen, TeleportAbsolute

POSE_TOLERANCE = 0.01
POSE_TIMEOUT = 5.0

class TurtleClient:
    def __init__(self, node: Node, cb_group: CallbackGroup):
        self.node = node
        self.set_pen_cli = node.create_client(SetPen, '/turtle1/set_pen', callback_group=cb_group)
        self.teleport_cli = node.create_client(
            TeleportAbsolute, '/turtle1/teleport_absolute', callback_group=cb_group
        )
        self.clear_cli = node.create_client(Empty, '/clear', callback_group=cb_group)

        self._pose = None
        self._cond = threading.Condition()
        node.create_subscription(Pose, '/turtle1/pose', self._on_pose, 10, callback_group=cb_group)

        self._pen = (255, 255, 255, 3)
        self.pen_is_down = True

    def _on_pose(self, msg: Pose) -> None:
        with self._cond:
            self._pose = msg
            self._cond.notify_all()

    def _near(self, x: float, y: float) -> bool:
        return (
            self._pose is not None
            and abs(self._pose.x - x) < POSE_TOLERANCE
            and abs(self._pose.y - y) < POSE_TOLERANCE
        )

    def _wait_until_at(self, x: float, y: float) -> bool:
        deadline = time.monotonic() + POSE_TIMEOUT
        with self._cond:
            while not self._near(x, y):
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    self.node.get_logger().warn(f'Pose tidak mencapai ({x:.2f}, {y:.2f})')
                    return False
                self._cond.wait(remaining)
        return True

    def wait_for_pose(self) -> None:

        with self._cond:
            while self._pose is None:
                self._cond.wait(1.0)

    def position(self):
        with self._cond:
            return (self._pose.x, self._pose.y) if self._pose else (None, None)

    def wait_for_services(self) -> None:

        for cli in (self.set_pen_cli, self.teleport_cli, self.clear_cli):
            while not cli.wait_for_service(timeout_sec=1.0):
                self.node.get_logger().info(f'Menunggu service {cli.srv_name} ...')

    def set_pen(self, r: int, g: int, b: int, width: int = 3, off: int = 0) -> None:

        req = SetPen.Request()
        req.r, req.g, req.b = int(r), int(g), int(b)
        req.width = int(width)
        req.off = int(off)
        self.set_pen_cli.call(req)
        self._pen = (int(r), int(g), int(b), int(width))
        self.pen_is_down = not off

    def pen_up(self) -> None:

        if self.pen_is_down:
            self.set_pen(*self._pen, off=1)

    def pen_down(self) -> None:

        if not self.pen_is_down:
            self.set_pen(*self._pen, off=0)

    def teleport(self, x: float, y: float, theta: float = 0.0) -> None:

        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = float(x), float(y), float(theta)
        self.teleport_cli.call(req)
        self._wait_until_at(x, y)

    def line_to(self, x: float, y: float, step: float = 0.05) -> None:

        x0, y0 = self.position()
        if x0 is None:
            self.teleport(x, y)
            return
        dist = math.hypot(x - x0, y - y0)
        n = max(1, math.ceil(dist / step)) if step > 0 else 1
        for i in range(1, n + 1):
            t = i / n
            self.teleport(x0 + (x - x0) * t, y0 + (y - y0) * t)

    def clear(self) -> None:

        self.clear_cli.call(Empty.Request())

def transition_to_next_cycle(turtle: TurtleClient) -> None:

    turtle.pen_up()
    turtle.clear()
    turtle.node.get_logger().info('Kanvas dibersihkan (/clear), siklus 2 dimulai')
