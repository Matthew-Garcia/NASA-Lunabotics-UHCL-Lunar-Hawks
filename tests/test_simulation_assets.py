"""Structural checks only; these do not substitute for Gazebo runtime tests."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
class SimulationAssets(unittest.TestCase):
    def test_tree_meshes_and_mechanisms(self):
        p=ROOT/'ros2_ws/src/lunabotics_description'
        root=ET.parse(p/'urdf/lunar_hawks.urdf').getroot()
        names={l.attrib['name'] for l in root.findall('link')}
        parents={j.find('child').attrib['link']:j.find('parent').attrib['link'] for j in root.findall('joint')}
        self.assertEqual(len(parents),len(names)-1)
        for n in names:
            seen=set()
            while n in parents:
                self.assertNotIn(n,seen);seen.add(n);n=parents[n]
            self.assertEqual(n,'base_link')
        for m in root.findall('.//mesh'):
            self.assertTrue((p/m.attrib['filename'].split('lunabotics_description/')[1]).is_file())
        for n in ['bucket_joint','rear_door_joint','excavator_deploy_joint','actuator_rod_left_joint','actuator_rod_right_joint','excavator_rod_left_joint','excavator_rod_right_joint']:
            self.assertIsNotNone(root.find(f"joint[@name='{n}']/limit"))
        self.assertIsNotNone(root.find("link[@name='rear_door']/collision"))
        self.assertEqual(root.find("joint[@name='rear_door_joint']/origin").attrib['xyz'],'0 0 .24')
        self.assertEqual(root.find("link[@name='rear_door']/inertial/origin").attrib['xyz'],'0 0 -.12')
        lidar_z=float(root.find("joint[@name='lidar_mount']/origin").attrib['xyz'].split()[2])
        self.assertGreaterEqual(lidar_z,.85)
    def test_four_posts_and_material(self):
        r=ET.parse(ROOT/'ros2_ws/src/lunabotics_description/worlds/arena.world').getroot()
        names=[m.attrib['name'] for m in r.findall('world/model')]
        self.assertEqual(sum(n.startswith('goal_post_') for n in names),4)
        self.assertEqual(sum(n.startswith('regolith_') for n in names),24)
    def test_wiring_phase_and_isolation_boundaries(self):
        rows=json.loads((ROOT/'docs/electrical/rev_c/module_connections.json').read_text())
        for ref,value,pins in rows:
            if 'BLDC CONTROLLER' in value:
                self.assertTrue({'PHASE_U','PHASE_V','PHASE_W'} <= {p[0] for p in pins})
            grounds={p[1] for p in pins} & {'MOTOR_GND','COMPUTE_GND'}
            if len(grounds)==2:self.assertIn('ISOLATED UART',value)
if __name__=='__main__':unittest.main()
