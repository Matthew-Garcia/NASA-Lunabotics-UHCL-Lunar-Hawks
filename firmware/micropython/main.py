import time
from machine import Pin, PWM
from microdot import Microdot
from microdot.websocket import with_websocket

# ==================================================
# PIN DEFINITIONS (same as Arduino)
# ==================================================

DIR_FR = Pin(2, Pin.OUT)
DIR_FL = Pin(4, Pin.OUT)
DIR_BR = Pin(5, Pin.OUT)
DIR_BL = Pin(13, Pin.OUT)

FR_PWM = PWM(Pin(18), freq=20000)
BR_PWM = PWM(Pin(19), freq=20000)
FL_PWM = PWM(Pin(32), freq=20000)
BL_PWM = PWM(Pin(33), freq=20000)

MOTOR_IN1 = Pin(25, Pin.OUT)
MOTOR_IN2 = Pin(26, Pin.OUT)

servoPin = Pin(12, Pin.OUT)
signalPin = Pin(23, Pin.OUT)

# ==================================================
# SAFE STARTUP
# ==================================================
def all_stop():
    FR_PWM.duty(0)
    BR_PWM.duty(0)
    FL_PWM.duty(0)
    BL_PWM.duty(0)

    DIR_FR.value(0)
    DIR_FL.value(0)
    DIR_BR.value(0)
    DIR_BL.value(0)

    MOTOR_IN1.value(0)
    MOTOR_IN2.value(0)
    servoPin.value(0)
    signalPin.value(0)

all_stop()
print("SAFE STARTUP: Motors OFF")

# ==================================================
# MOTOR CONTROL HELPERS
# ==================================================
def set_pwm(pwm, val):
    duty = min(max(int(val), 0), 255)
    pwm.duty(duty)

# ==================================================
# FORWARD / BACKWARD (unchanged)
# ==================================================
def forward(power):
    set_pwm(FR_PWM, power * 1.2)
    set_pwm(BR_PWM, power)
    set_pwm(FL_PWM, power * 1.8)
    set_pwm(BL_PWM, power)

    DIR_FR.value(1)
    DIR_FL.value(1)
    DIR_BR.value(0)
    DIR_BL.value(0)

def backward(power):
    set_pwm(FR_PWM, power * 1.8)
    set_pwm(BR_PWM, power * 1.5)
    set_pwm(FL_PWM, power / 1.2)
    set_pwm(BL_PWM, power / 1.5)

    DIR_FR.value(0)
    DIR_FL.value(0)
    DIR_BR.value(1)
    DIR_BL.value(1)

# ==================================================
# UPDATED TANK TURNING (NEW)
# ==================================================
def tankLeft(power):
    print("TANK LEFT")

    # RIGHT wheels forward
    set_pwm(FR_PWM, power)
    set_pwm(BR_PWM, power)
    DIR_FR.value(1)
    DIR_BR.value(1)

    # LEFT wheels reverse
    set_pwm(FL_PWM, power)
    set_pwm(BL_PWM, power)
    DIR_FL.value(1)
    DIR_BL.value(1)

def tankRight(power):
    print("TANK RIGHT")

    # LEFT wheels forward
    set_pwm(FL_PWM, power)
    set_pwm(BL_PWM, power)
    DIR_FL.value(0)
    DIR_BL.value(0)

    # RIGHT wheels reverse
    set_pwm(FR_PWM, power)
    set_pwm(BR_PWM, power)
    DIR_FR.value(0)
    DIR_BR.value(0)

# ==================================================
# OLD ARC TURNING (no longer used, but kept)
# ==================================================
def leftforward(power):
    set_pwm(FR_PWM, power)
    set_pwm(BR_PWM, power)
    set_pwm(FL_PWM, 0)
    set_pwm(BL_PWM, 0)

    DIR_FR.value(1)
    DIR_FL.value(1)
    DIR_BR.value(0)
    DIR_BL.value(0)

def rightforward(power):
    set_pwm(FR_PWM, 0)
    set_pwm(BR_PWM, 0)
    set_pwm(FL_PWM, power * 1.5)
    set_pwm(BL_PWM, power * 1.5)

    DIR_FR.value(1)
    DIR_FL.value(1)
    DIR_BR.value(0)
    DIR_BL.value(0)

# ==================================================
# GENERAL CONTROL
# ==================================================
def stop():
    all_stop()

def up():
    MOTOR_IN1.value(1)
    MOTOR_IN2.value(0)

def down():
    MOTOR_IN1.value(0)
    MOTOR_IN2.value(1)

def dump():
    servoPin.value(1)

# ==================================================
# WEBSOCKET SERVER
# ==================================================

POWER = 40

app = Microdot()

@app.route("/")
def index(req):
    return "ESP32 Rover Ready"

@app.route("/ws")
@with_websocket
async def ws_handler(req, ws):
    print("WS connected")

    while True:
        msg = await ws.receive()
        if msg is None:
            break

        msg = msg.strip()
        print("RX:", msg)

        # Driving
        if msg == "FWD":
            forward(POWER)
        elif msg == "BACK":
            backward(POWER)
        elif msg == "LEFT":
            tankLeft(POWER)        # *** NEW TANK LEFT ***
        elif msg == "RIGHT":
            tankRight(POWER)       # *** NEW TANK RIGHT ***
        elif msg == "STOP":
            stop()

        # Actuator
        elif msg == "RB":
            up()
        elif msg == "LB":
            down()

        # Dump
        elif msg == "triangle":
            dump()

        # Extra signal pin
        elif msg == "X":
            signalPin.value(1)

        await ws.send("ACK")

    all_stop()
    print("WS disconnected")

print("Microdot running on 0.0.0.0:81")
app.run(host="0.0.0.0", port=81)
