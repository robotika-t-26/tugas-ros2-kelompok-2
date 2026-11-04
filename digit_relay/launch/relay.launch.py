# Master launch file: turtlesim + 6 node anggota.

# Anggota : Nabila Shafa Rahayu - 5025241150

# Pemakaian:
#   ros2 launch digit_relay relay.launch.py
#   ros2 launch digit_relay relay.launch.py shutdown_on_finish:=true

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

NUM_MEMBERS = 6


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('digit_relay'), 'config', 'members.yaml'
    )

    turtlesim = Node(package='turtlesim', executable='turtlesim_node', name='turtlesim')

    members = [
        Node(
            package='digit_relay',
            executable=f'member{i}',
            name=f'member{i}',          # harus sama dengan kunci di members.yaml
            parameters=[config],
            output='screen',
        )
        for i in range(1, NUM_MEMBERS + 1)
    ]

    return LaunchDescription([turtlesim, *members])
