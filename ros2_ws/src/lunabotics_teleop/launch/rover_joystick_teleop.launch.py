"""Launch joystick mapping onto a preview topic by default."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Resolve configuration without a machine-specific path."""
    config = os.path.join(
        get_package_share_directory('lunabotics_teleop'),
        'config', 'joy_teleop.yaml')
    return LaunchDescription([
        DeclareLaunchArgument(
            'command_topic', default_value='/lunabotics/cmd_vel_preview'),
        Node(package='joy', executable='joy_node', name='joystick'),
        Node(
            package='joy_teleop', executable='joy_teleop', name='joy_teleop',
            parameters=[config],
            remappings=[('/cmd_vel', LaunchConfiguration('command_topic'))]),
    ])
