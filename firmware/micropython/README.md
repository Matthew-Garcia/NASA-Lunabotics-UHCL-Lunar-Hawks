# MicroPython: three-file dry-run prototype

**New AI-assisted examples, not recovered historical rover firmware. No GPIO/PWM output implementation is included.** micro-ROS and MicroPython are alternative MCU firmware images.

| File | Purpose |
| --- | --- |
| boot.py | Inert startup notice; no automatic Wi-Fi/server or GPIO |
| test.py | Portable logic self-test without networking or physical motion |
| main.py | Limited WebSocket server, validated normalized command mixer, dry-run timeout state |

## Host demo

~~~bash
python3 firmware/micropython/test.py
python3 firmware/micropython/main.py
~~~

Connect a WebSocket client to ws://127.0.0.1:8765/control and send:

~~~json
{"v":0.25,"w":0.0,"deadman":true}
~~~

Replies report dry_run, left, and right. Inputs are normalized [-1,1], NOT m/s, rad/s, or PWM duty. Send at about 10 Hz for a sustained demo. Deadman false clears the request; malformed commands/disconnect clear it; a 500 ms no-valid-command interval clears it via the watchdog. This is software-only state and is not a safety-rated stop.

## On an ESP32

Install the appropriate MicroPython image only after backing up existing firmware and disconnecting motor power. Copy these three files to the board. At the REPL, configure a private lab Wi-Fi connection manually (do not commit credentials), import main and asyncio, then explicitly run asyncio.run(main.serve(host="<board-private-IP>")). Target execution is not yet verified.

boot.py deliberately does not touch pins; it cannot guarantee safe physical output levels. Hardware inhibit must hold drivers disabled. A separate, reviewed motor adapter, hardware interlocks, pin mapping, output fault handling, and target tests are required before any physical control.

## Protocol limits and security

One active client. Only masked, unfragmented text frames of at most 125 bytes; close/ping/pong supported, no binary, compression, or extended-length frames. Full HTTP header capped at 2048 bytes and two seconds. Frame reads bounded to 500 ms. Not a general-purpose WebSocket stack. No authentication or TLS; localhost or isolated lab network only. Do not expose to the internet or attach actuator outputs.

API references: [MicroPython ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html) and [asyncio](https://docs.micropython.org/en/latest/library/asyncio.html). These upstream pages describe the development branch; pin and test the deployed interpreter before relying on target compatibility.
