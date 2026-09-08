"""Repository structure checks; no external services or hardware required."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_relative_markdown_links(self):
        for document in ROOT.rglob('*.md'):
            if '.git' in document.parts:
                continue
            content = document.read_text()
            for target in re.findall(r'\]\(([^)]+)\)', content):
                if '://' in target or target.startswith('#'):
                    continue
                target = unquote(target.split('#')[0])
                self.assertTrue((document.parent / target).exists(),
                                '{} -> {}'.format(document, target))

    def test_ros_dependencies_declared(self):
        package = ET.parse(ROOT / 'ros2_ws/src/lunabotics_teleop/package.xml')
        deps = {node.text for node in package.findall('exec_depend')}
        self.assertTrue({'joy', 'joy_teleop', 'launch', 'launch_ros',
                         'ament_index_python', 'geometry_msgs'} <= deps)

    def test_preview_topic_default_and_no_old_home_path(self):
        path = ROOT / 'ros2_ws/src/lunabotics_teleop/launch/rover_joystick_teleop.launch.py'
        content = path.read_text()
        self.assertIn('/lunabotics/cmd_vel_preview', content)
        self.assertNotIn('/home/uhcl_lunabotics', content)

    def test_three_micropython_files(self):
        names = {p.name for p in (ROOT / 'firmware/micropython').glob('*.py')}
        self.assertEqual(names, {'boot.py', 'test.py', 'main.py'})
