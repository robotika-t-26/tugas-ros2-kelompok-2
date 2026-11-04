# Master launch file: turtlesim + 6 node anggota.

# Anggota : Nabila Shafa Rahayu - 5025241150

# Pemakaian:
#   ros2 launch digit_relay relay.launch.py
#   ros2 launch digit_relay relay.launch.py shutdown_on_finish:=true

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

NUM_MEMBERS = 6


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('digit_relay'), 'config', 'members.yaml'
    )

    shutdown_arg = DeclareLaunchArgument(
        'shutdown_on_finish', default_value='false',
        description='Tutup seluruh sistem setelah relay selesai',
    )

    turtlesim = Node(package='turtlesim', executable='turtlesim_node', name='turtlesim')

    members = [
        Node(
            package='digit_relay',
            executable=f'member{i}',
            name=f'member{i}',      
            parameters=[config],
            output='screen',
        )
        for i in range(1, NUM_MEMBERS + 1)
    ]

    shutdown_on_last_exit = RegisterEventHandler(
        OnProcessExit(
            target_action=members[-1],
            on_exit=[EmitEvent(event=Shutdown(reason='Relay selesai'))],
        ),
        condition=IfCondition(LaunchConfiguration('shutdown_on_finish')),
    )

    return LaunchDescription([shutdown_arg, turtlesim, *members, shutdown_on_last_exit])
