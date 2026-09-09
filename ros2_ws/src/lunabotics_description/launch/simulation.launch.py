from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node

def generate_launch_description():
    p=Path(get_package_share_directory('lunabotics_description'))
    g=Path(get_package_share_directory('gazebo_ros'))
    return LaunchDescription([
        DeclareLaunchArgument('autonomy', default_value='false'),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(g/'launch/gazebo.launch.py')),launch_arguments={'world':str(p/'worlds/arena.world')}.items()),
        Node(package='robot_state_publisher',executable='robot_state_publisher',parameters=[{'robot_description':(p/'urdf/lunar_hawks.urdf').read_text(),'use_sim_time':True}]),
        Node(package='gazebo_ros',executable='spawn_entity.py',arguments=['-entity','lunar_hawks','-topic','robot_description','-x','0','-y','0','-z','.27']),
        Node(package='rviz2',executable='rviz2',arguments=['-d',str(p/'config/rover.rviz')],parameters=[{'use_sim_time':True}]),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(Path(get_package_share_directory('lunabotics_autonomy'))/'launch/autonomy.launch.py')),condition=IfCondition(LaunchConfiguration('autonomy')))
    ])
