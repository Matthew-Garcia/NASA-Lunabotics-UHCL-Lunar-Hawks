# Hardware bring-up gates

This is not a safety-certified control system. Software zero commands and joystick deadman buttons do not replace a wired emergency stop that independently disables hazardous motion.

1. Identify the actual MCU, drivers, connector pinouts, signal levels, boot states, supply maximums, and grounding/isolation scheme.
2. Check GPIOs against the correct MCU datasheet, including boot-strapping and flash/PSRAM pins.
3. With motor power disconnected, verify startup, reset, brownout, firmware error, joystick release, controller disconnect, serial loss, malformed input, and MCU hang behavior.
4. Scope outputs into dummy loads; verify PWM frequency, polarity, duty limits, enable behavior, and direction-change interlocks.
5. Independently verify a wired emergency-stop/driver-disable chain. Require deliberate local reset after faults, with no automatic restart.
6. Verify fuses, wire gauge, connectors, transient protection, current limits, and thermal behavior from actual loads.
7. After review, conduct restrained low-energy tests with mechanisms clear of people. Record exact revisions and results.

The preserved C firmware lacks a last-command timeout and explicit finite-input rejection. Error paths can terminate a task without first forcing outputs off. GPIO/LEDC call errors are not checked. Do not deploy it unchanged as a fail-safe controller. New MicroPython examples intentionally contain no motor-output implementation.
