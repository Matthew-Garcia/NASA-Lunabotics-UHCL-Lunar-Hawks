"""KiCad 9 system wiring schematic with explicit module boundaries and named nets."""
from pathlib import Path
import uuid,json
R=Path(__file__).resolve().parents[1]
P=R/'docs/electrical/rev_c';P.mkdir(parents=True,exist_ok=True)
def uid():return str(uuid.uuid4())
def q(s):return json.dumps(str(s))
root_id=uid();lib=[];instances=[];wires=[];labels=[]
components=[
 ('BT1','24V MOTOR BATTERY',[('PLUS','BAT24_RAW'),('MINUS','MOTOR_GND')]),
 ('F1','MAIN FUSE - SIZE TBD',[('IN','BAT24_RAW'),('OUT','BAT24_FUSED')]),
 ('K1','DC CONTACTOR - RATING TBD',[('POWER_IN','BAT24_FUSED'),('POWER_OUT','MOTOR24'),('COIL_PLUS','ESTOP_COIL'),('COIL_MINUS','MOTOR_GND')]),
 ('SW1','LATCHING E-STOP NC',[('IN','BAT24_FUSED'),('OUT','ESTOP_COIL')]),
 ('BT2','V-MOUNT COMPUTE BATTERY',[('PLUS','COMPUTE_RAW'),('MINUS','COMPUTE_GND')]),
 ('F2','COMPUTE FUSE - SIZE TBD',[('IN','COMPUTE_RAW'),('OUT','COMPUTE_FUSED')]),
 ('U1','CARRIER INPUT PROTECTION / DC-DC',[('IN_PLUS','COMPUTE_FUSED'),('IN_RETURN','COMPUTE_GND'),('OUT_PLUS','JETSON_INPUT'),('OUT_RETURN','COMPUTE_GND')]),
 ('U2','JETSON ORIN NX CARRIER - MODEL TBD',[('VIN','JETSON_INPUT'),('GND','COMPUTE_GND'),('UART_TX_3V3','JETSON_TX'),('UART_RX_3V3','JETSON_RX'),('USB_LIDAR','USB_LIDAR'),('USB_CAMERA','USB_CAMERA')]),
 ('U3','ISOLATED UART MODULE 115200',[('A_VCC','COMPUTE_3V3'),('A_GND','COMPUTE_GND'),('A_TX','JETSON_TX'),('A_RX','JETSON_RX'),('B_VCC','LOGIC_3V3'),('B_GND','MOTOR_GND'),('B_RX','ESP32_RX'),('B_TX','ESP32_TX')]),
 ('U4','COMPUTE 3V3 REGULATOR MODULE',[('IN','JETSON_INPUT'),('RETURN','COMPUTE_GND'),('OUT','COMPUTE_3V3')]),
 ('F3','LOGIC FUSE - SIZE TBD',[('IN','BAT24_FUSED'),('OUT','LOGIC_INPUT')]),
 ('U5','24V TO 3V3 REGULATOR MODULE',[('VIN','LOGIC_INPUT'),('GND','MOTOR_GND'),('VOUT','LOGIC_3V3')]),
 ('U6','ESP32 WROOM INTERFACE - GPIO TBD',[('VCC','LOGIC_3V3'),('GND','MOTOR_GND'),('RX','ESP32_RX'),('TX','ESP32_TX'),('LEFT_PWM','LEFT_PWM'),('LEFT_DIR','LEFT_DIR'),('RIGHT_PWM','RIGHT_PWM'),('RIGHT_DIR','RIGHT_DIR'),('CONVEYOR','CONVEYOR_PWM'),('BUCKET_UP','BUCKET_UP'),('BUCKET_DOWN','BUCKET_DOWN'),('LIFT_UP','LIFT_UP'),('LIFT_DOWN','LIFT_DOWN')]),
]
for i,side in enumerate(['FL','FR','RL','RR']):
 sig='LEFT' if side.endswith('L') else 'RIGHT'
 components.extend([(f'F{10+i}',side+' BRANCH FUSE - TBD',[('IN','MOTOR24'),('OUT',side+'_24')]),
  (f'U{10+i}',side+' EXTERNAL BLDC CONTROLLER',[('VIN',side+'_24'),('GND','MOTOR_GND'),('PWM',sig+'_PWM'),('DIR',sig+'_DIR'),('PHASE_U',side+'_U'),('PHASE_V',side+'_V'),('PHASE_W',side+'_W')]),
  (f'M{1+i}',side+' BLDC MOTOR',[('U',side+'_U'),('V',side+'_V'),('W',side+'_W')])])
for i,(name,ctrl) in enumerate([('CONVEYOR',['CONVEYOR_PWM']),('BUCKET',['BUCKET_UP','BUCKET_DOWN']),('LIFT',['LIFT_UP','LIFT_DOWN'])]):
 components.append((f'F{20+i}',name+' FUSE - TBD',[('IN','MOTOR24'),('OUT',name+'_24')]))
 components.append((f'U{20+i}',name+' EXTERNAL BRUSHED DRIVER',[('VIN',name+'_24'),('GND','MOTOR_GND')]+[(n,n) for n in ctrl]+[('OUT_A',name+'_A'),('OUT_B',name+'_B')]))
 components.append((f'J{20+i}',name+(' MOTOR' if i==0 else ' ACTUATOR PAIR; SYNC REQUIRED'),[('A',name+'_A'),('B',name+'_B')]))
# Independent electronic latch driver and feedback; no powered rear-door motor.
components.extend([
 ('F23','LATCH BRANCH FUSE - TBD',[('IN','MOTOR24'),('OUT','LATCH_24')]),
 ('U23','LATCH SOLENOID DRIVER + CLAMP - TBD',[('VIN','LATCH_24'),('GND','MOTOR_GND'),('RELEASE_3V3','LATCH_RELEASE'),('OUT','LATCH_SW')]),
 ('Y1','ELECTRONIC LATCH - COIL VOLTAGE TBD',[('PLUS','LATCH_24'),('SW_RETURN','LATCH_SW')]),
 ('J23','DOOR / LATCH FEEDBACK INTERFACE',[('DOOR_CLOSED','DOOR_CLOSED'),('LATCH_ENGAGED','LATCH_ENGAGED'),('GND','MOTOR_GND')]),
 ('U24','ESP32 FEEDBACK / LATCH GPIO ASSIGNMENTS TBD',[('RELEASE','LATCH_RELEASE'),('CLOSED_INPUT','DOOR_CLOSED'),('ENGAGED_INPUT','LATCH_ENGAGED'),('BUCKET_LOWERED','BUCKET_LOWERED'),('EXCAVATOR_STOWED','EXCAVATOR_STOWED'),('EXCAVATOR_DEPLOYED','EXCAVATOR_DEPLOYED')]),
 ('J24','ACTUATOR ENDPOINT FEEDBACK',[('BUCKET_LOWERED','BUCKET_LOWERED'),('EXCAVATOR_STOWED','EXCAVATOR_STOWED'),('EXCAVATOR_DEPLOYED','EXCAVATOR_DEPLOYED'),('GND','MOTOR_GND')]),
])
# Large sheet keeps every module legible without text overlap.
for index,(ref,value,pins) in enumerate(components):
 x=48+(index%5)*110;y=38+(index//5)*78;h=max(12,len(pins)*2.54+5);key='Module_'+ref
 ps=''
 for j,(name,net) in enumerate(pins):
  py=-j*2.54
  ps+=f'(pin passive line (at -25.4 {py} 0)(length 5.08)(name {q(name)} (effects(font(size 1 1))))(number "{j+1}" (effects(font(size 1 1)))))'
  wy=y+j*2.54
  wires.append(f'(wire(pts(xy {x-25.4} {wy})(xy {x-43.18} {wy}))(stroke(width 0)(type default))(uuid "{uid()}"))')
  labels.append(f'(label {q(net)} (at {x-43.18} {wy} 0)(effects(font(size .9 .9))(justify left bottom))(uuid "{uid()}"))')
 lib.append(f'(symbol "{key}" (pin_names(offset .5))(in_bom yes)(on_board no)(property "Reference" "{ref}" (at 0 5 0)(effects(font(size 1 1))))(property "Value" {q(value)} (at 0 2 0)(effects(font(size 1 1))))(symbol "{key}_0_1"(rectangle(start -20.32 2.54)(end 48 {-h})(stroke(width .254)(type default))(fill(type background))))(symbol "{key}_1_1"{ps}))')
 puid=uid()
 instances.append(f'(symbol(lib_id "{key}")(at {x} {y} 0)(unit 1)(in_bom yes)(on_board no)(dnp no)(uuid "{puid}")(property "Reference" "{ref}" (at {x} {y-6} 0)(effects(font(size 1.27 1.27))))(property "Value" {q(value)} (at {x+10} {y-3} 0)(effects(font(size 1 1))))'+''.join(f'(pin "{j+1}"(uuid "{uid()}"))' for j in range(len(pins)))+f'(instances(project "Lunar_Hawks_RevC"(path "/{root_id}"(reference "{ref}")(unit 1)))))')
notes='Engineering system wiring draft. Module ports are logical, NOT connector pin assignments.\nSelect real modules, protection ratings and contactor coil suppression before fabrication.\nIsolated UART: no MOTOR_GND to COMPUTE_GND connection. Verify USB shields do not bypass isolation.\nActuator synchronization, limit switches, driver input thresholds and watchdog remain design gates.'
out=f'(kicad_sch(version 20250114)(generator "eeschema")(uuid "{root_id}")(paper "User" 594 841)(title_block(title "Lunar Hawks Rev C.1 - Top Hinged Door and Four Actuators")(rev "C.1"))(lib_symbols {"".join(lib)})'+''.join(wires+labels+instances)+f'(text {q(notes)} (at 20 750 0)(effects(font(size 2 2))(justify left top))(uuid "{uid()}")))'
(P/'Lunar_Hawks_RevC.kicad_sch').write_text(out)
(P/'module_connections.json').write_text(json.dumps(components,indent=2))
