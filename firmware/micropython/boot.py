import network, time
from machine import Pin

# ====== CRITICAL SAFETY: Force all robot pins LOW at boot =======
motor_pins = [2, 4, 5, 13, 18, 19, 32, 33, 23, 12, 25, 26]

for p in motor_pins:
    try:
        Pin(p, Pin.OUT).value(0)
    except:
        pass

print("All motor pins forced LOW at boot for safety.")

# ====== WiFi connection ======
SSID = "Team23"
PASSWORD = "uhclgambit"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected! IP:", wlan.ifconfig()[0])

