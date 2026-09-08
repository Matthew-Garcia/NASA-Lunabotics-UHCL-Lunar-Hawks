"""Inert startup for the NEW dry-run prototype; not historical rover firmware.

No GPIO, PWM, Wi-Fi credentials, automatic networking, or motor enable.
Use external hardware inhibit: leaving pins untouched is NOT a safe-stop circuit.
"""
print("Lunar Hawks: dry-run only. No motor outputs or network started.")
