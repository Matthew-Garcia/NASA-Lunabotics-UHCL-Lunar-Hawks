# Migration-time validation — 2026-09-08

| Check | Result | Scope |
| --- | --- | --- |
| MicroPython-compatible self-test | PASS | CPython host only |
| unittest discovery | PASS: 14 tests | Command validation/mixing, deadman, timeout, WebSocket handshake/framing/local socket, links and ROS metadata |
| Python compileall | PASS | Python syntax, not ROS imports or MCU compatibility |
| git diff --check | PASS before commit | Whitespace hygiene |
| Original C application / colcon metadata | Byte-identical to source | Preserved, not rebuilt |
| Original software PDF | Byte-identical to source | Historical documentation, not publication manuscript |
| ROS 2 runtime and build | NOT RUN | Target ROS environment unavailable |
| ESP32 / MicroPython target execution | NOT RUN | Hardware unavailable |
| PCB ERC / DRC / electrical test | NOT RUN | Concept documentation only; schematic/layout not designed |

Host checks are also configured in .github/workflows/host-checks.yml. A workflow definition is not proof of a completed GitHub Actions run. This report does not assert physical performance or safe deployment.
