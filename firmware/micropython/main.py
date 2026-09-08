"""Limited WebSocket dry-run server for CPython/MicroPython; NO GPIO outputs.

Single client, <=125-byte masked, unfragmented text messages. No TLS/auth.
Bind to localhost for host tests; private lab network only on an ESP32.
Do not turn this into a physical controller without a separate safety design.
"""
import asyncio
import binascii
import hashlib
import json
import math
import sys
import time

GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
TIMEOUT_MS = 500


def now_ms():
    if hasattr(time, "ticks_ms"):
        return time.ticks_ms()
    return int(time.monotonic() * 1000)


def elapsed_ms(now, then):
    if hasattr(time, "ticks_diff"):
        return time.ticks_diff(now, then)
    return now - then


def parse_command(payload):
    """Require explicit deadman and finite normalized v/w values."""
    obj = json.loads(payload)
    if not isinstance(obj, dict) or set(obj) != {"v", "w", "deadman"}:
        raise ValueError("Expected only v, w and deadman")
    if type(obj["deadman"]) is not bool:
        raise ValueError("deadman must be boolean")
    for name in ("v", "w"):
        value = obj[name]
        if type(value) not in (int, float):
            raise ValueError("v and w must be numbers, not booleans")
        if not math.isfinite(value) or not -1.0 <= value <= 1.0:
            raise ValueError("v and w must be finite and within [-1, 1]")
    if not obj["deadman"]:
        return 0.0, 0.0
    return float(obj["v"]), float(obj["w"])


def mix(v, w):
    """Normalized arcade mixer, NOT calibrated velocity or PWM units."""
    left, right = v - w, v + w
    scale = max(1.0, abs(left), abs(right))
    return left / scale, right / scale


class DryRunController:
    """Records normalized left/right requests only; cannot drive hardware."""

    def __init__(self):
        self.outputs = (0.0, 0.0)
        self.last_ms = None

    def stop(self):
        self.outputs = (0.0, 0.0)
        self.last_ms = None

    def receive(self, payload, stamp):
        try:
            self.outputs = mix(*parse_command(payload))
            self.last_ms = stamp
        except (ValueError, TypeError, OverflowError):
            self.stop()
            raise
        return self.outputs

    def expire(self, stamp):
        if self.last_ms is not None:
            if elapsed_ms(stamp, self.last_ms) >= TIMEOUT_MS:
                self.stop()
        return self.outputs


def accept_key(key):
    raw = binascii.a2b_base64(key)
    if len(raw) != 16:
        raise ValueError("Invalid WebSocket key")
    return binascii.b2a_base64(hashlib.sha1(key + GUID).digest()).strip()


async def handshake(reader, writer):
    """Bound the full HTTP header to 2048 bytes; caller bounds duration."""
    header = bytearray()
    while not header.endswith(b"\r\n\r\n"):
        if len(header) >= 2048:
            raise ValueError("Header too large")
        header.extend(await reader.readexactly(1))
    lines = bytes(header).split(b"\r\n")
    if lines[0] != b"GET /control HTTP/1.1":
        raise ValueError("Use /control")
    fields = {}
    for line in lines[1:]:
        if line:
            name, value = line.split(b":", 1)
            name = name.strip().lower()
            if name in fields:
                raise ValueError("Duplicate header")
            fields[name] = value.strip()
    connection = [s.strip().lower() for s in fields.get(b"connection", b"").split(b",")]
    if (fields.get(b"upgrade", b"").lower() != b"websocket"
            or b"upgrade" not in connection
            or fields.get(b"sec-websocket-version") != b"13"):
        raise ValueError("Invalid upgrade")
    key = accept_key(fields.get(b"sec-websocket-key", b""))
    writer.write(b"HTTP/1.1 101 Switching Protocols\r\n"
                 b"Upgrade: websocket\r\nConnection: Upgrade\r\n"
                 b"Sec-WebSocket-Accept: " + key + b"\r\n\r\n")
    await writer.drain()


async def read_frame(reader):
    """Deliberately supports only short FIN frames, without extensions."""
    first, second = await reader.readexactly(2)
    opcode, length = first & 15, second & 127
    if not first & 128 or first & 112 or not second & 128:
        raise ValueError("Requires FIN, no extensions, and masking")
    if opcode not in (1, 8, 9, 10) or length > 125:
        raise ValueError("Unsupported frame")
    mask = await reader.readexactly(4)
    data = await reader.readexactly(length)
    return opcode, bytes(x ^ mask[i % 4] for i, x in enumerate(data))


class DryRunServer:
    """A second connection cannot take ownership or stop an active client."""

    def __init__(self):
        self.controller = DryRunController()
        self.busy = False

    async def handle(self, reader, writer):
        if self.busy:
            writer.close()
            await writer.wait_closed()
            return
        self.busy = True
        try:
            await asyncio.wait_for(handshake(reader, writer), 2.0)
            while True:
                # Short timeout includes the whole frame, not each byte.
                opcode, payload = await asyncio.wait_for(read_frame(reader), 0.5)
                if opcode == 8:
                    writer.write(b"\x88\x00")
                    await writer.drain()
                    break
                if opcode == 9:
                    writer.write(bytes((138, len(payload))) + payload)
                    await writer.drain()
                elif opcode == 1:
                    result = self.controller.receive(payload.decode("utf-8"), now_ms())
                    reply = json.dumps({"dry_run": True, "left": result[0],
                                        "right": result[1]}).encode()
                    writer.write(bytes((129, len(reply))) + reply)
                    await writer.drain()
        except (Exception,):
            # Any malformed input, disconnect or timeout clears dry-run state.
            pass
        finally:
            self.controller.stop()
            writer.close()
            try:
                await writer.wait_closed()
            finally:
                self.busy = False

    async def watchdog(self):
        while True:
            self.controller.expire(now_ms())
            await asyncio.sleep(0.02)


async def serve(host="127.0.0.1", port=8765):
    service = DryRunServer()
    watchdog = asyncio.create_task(service.watchdog())
    server = await asyncio.start_server(service.handle, host, port)
    print("DRY RUN WebSocket on", host, port, "/control")
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        watchdog.cancel()
        server.close()
        await server.wait_closed()
        service.controller.stop()


if __name__ == "__main__":
    if sys.implementation.name == "micropython":
        print("Dry-run main.py loaded. Start serve() explicitly at the REPL.")
    else:
        asyncio.run(serve())
