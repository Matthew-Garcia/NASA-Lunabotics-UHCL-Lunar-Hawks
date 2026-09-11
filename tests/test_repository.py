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

    def test_micropython_programs_and_host_test_module(self):
        names = {p.name for p in (ROOT / 'firmware/micropython').glob('*.py')}
        self.assertEqual(names, {'boot.py', 'test.py', 'main.py', 'dry_run.py'})

    def test_cad_assets_remain_grouped_by_provenance(self):
        cad = ROOT / 'cad'
        original = {
            '12_inch+Linear+actuator.stl', '12mm+Sprocket.stl',
            'Bucket+#1.stl', 'Door+Frame.stl', 'Hatch+Design.stl',
        }
        self.assertEqual({p.name for p in cad.glob('*.stl')}, original)
        self.assertTrue((cad / 'full_rover/wheel_300mm_lab.stl').is_file())
        self.assertTrue((cad / 'full_rover/bucket.stl').is_file())
        self.assertTrue((cad / 'autonomy_rover/goal_post.stl').is_file())
