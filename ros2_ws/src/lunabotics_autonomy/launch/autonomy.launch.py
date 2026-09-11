from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='lunabotics_autonomy', executable='goal_post_detector', output='screen', parameters=[{'use_sim_time':True,'simulation_mission':True}]),
        Node(package='lunabotics_autonomy', executable='regolith_detector', output='screen', parameters=[{'use_sim_time':True,'simulation_mission':True}]),
        Node(package='lunabotics_autonomy', executable='lidar_safety', output='screen', parameters=[{'use_sim_time':True,'simulation_mission':True}]),
        Node(package='lunabotics_autonomy', executable='mission_manager', output='screen', parameters=[{'use_sim_time':True,'simulation_mission':True}]),
    ])
