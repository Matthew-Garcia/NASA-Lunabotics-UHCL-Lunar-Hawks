from setuptools import setup
from glob import glob
import os

package_name = 'lunabotics_autonomy'
setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={'console_scripts': [
        'goal_post_detector = lunabotics_autonomy.goal_post_detector:main',
        'lidar_safety = lunabotics_autonomy.lidar_safety:main',
        'mission_manager = lunabotics_autonomy.mission_manager:main',
        'regolith_detector = lunabotics_autonomy.regolith_detector:main',
    ]},
)
