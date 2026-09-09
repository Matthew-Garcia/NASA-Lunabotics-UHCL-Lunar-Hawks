"""Host-only tests: protocol behavior is not physical rover validation."""
import asyncio
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ws", ROOT / "firmware/micropython/dry_run.py")
ws = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ws)


def frame(payload, opcode=1):
    data = payload.encode() if isinstance(payload, str) else payload
    mask = b"abcd"
    return bytes((128 | opcode, 128 | len(data))) + mask + bytes(
        value ^ mask[i % 4] for i, value in enumerate(data))


class CommandTests(unittest.TestCase):
    def test_forward_reverse_turn(self):
        self.assertEqual(ws.mix(1, 0), (1, 1))
        self.assertEqual(ws.mix(-1, 0), (-1, -1))
        self.assertEqual(ws.mix(0, 1), (-1, 1))

    def test_saturation_preserves_ratio(self):
        left, right = ws.mix(1, 1)
        self.assertEqual((left, right), (0, 1))

    def test_deadman(self):
        self.assertEqual(ws.parse_command(
            '{"v":1,"w":1,"deadman":false}'), (0, 0))

    def test_bad_input_stops(self):
        values = ({}, [], {"v": True, "w": 0, "deadman": True},
                  {"v": 2, "w": 0, "deadman": True},
                  {"v": 0, "w": 0, "deadman": 1},
                  {"v": float("nan"), "w": 0, "deadman": True},
                  {"v": float("inf"), "w": 0, "deadman": True},
                  {"v": 0, "w": 0, "deadman": True, "extra": 1})
        for value in values:
            controller = ws.DryRunController()
            controller.receive('{"v":1,"w":0,"deadman":true}', 10)
            with self.assertRaises((ValueError, TypeError, OverflowError)):
                controller.receive(json.dumps(value), 20)
            self.assertEqual(controller.outputs, (0, 0))

    def test_timeout_boundary(self):
        controller = ws.DryRunController()
        controller.receive('{"v":1,"w":0,"deadman":true}', 100)
        self.assertEqual(controller.expire(599), (1, 1))
        self.assertEqual(controller.expire(600), (0, 0))

    def test_standard_accept_key(self):
        self.assertEqual(ws.accept_key(b"dGhlIHNhbXBsZSBub25jZQ=="),
                         b"s3pPLMBiTxaQ9kYGzzhZRbK+xOo=")


class WebSocketTests(unittest.IsolatedAsyncioTestCase):
    async def test_frame_decode(self):
        reader = asyncio.StreamReader()
        reader.feed_data(frame('{"v":0,"w":0,"deadman":false}'))
        self.assertEqual((await ws.read_frame(reader))[0], 1)

    async def test_reject_unmasked_fragmented_extended_binary(self):
        for data in (b"\x81\x00", b"\x01\x80", b"\x81\xfe", b"\x82\x80"):
            reader = asyncio.StreamReader()
            reader.feed_data(data)
            with self.assertRaises(ValueError):
                await ws.read_frame(reader)

    async def test_real_socket_upgrade_command_close(self):
        service = ws.DryRunServer()
        server = await asyncio.start_server(service.handle, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        reader, writer = await asyncio.open_connection("127.0.0.1", port)
        try:
            writer.write(
                b"GET /control HTTP/1.1\r\nHost: localhost\r\n"
                b"Upgrade: websocket\r\nConnection: Upgrade\r\n"
                b"Sec-WebSocket-Version: 13\r\n"
                b"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n\r\n")
            await writer.drain()
            header = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 1)
            self.assertIn(b"101 Switching Protocols", header)
            writer.write(frame('{"v":0.5,"w":0,"deadman":true}'))
            await writer.drain()
            first, size = await asyncio.wait_for(reader.readexactly(2), 1)
            self.assertEqual(first, 129)
            reply = json.loads(await reader.readexactly(size))
            self.assertTrue(reply["dry_run"])
            self.assertEqual(reply["left"], 0.5)
            writer.write(frame(b"", opcode=8))
            await writer.drain()
            self.assertEqual(await reader.readexactly(2), b"\x88\x00")
            await reader.read()
            self.assertEqual(service.controller.outputs, (0, 0))
        finally:
            writer.close()
            await writer.wait_closed()
            server.close()
            await server.wait_closed()

    async def test_watchdog_expires_even_without_network(self):
        service = ws.DryRunServer()
        service.controller.receive('{"v":1,"w":0,"deadman":true}',
                                   ws.now_ms() - ws.TIMEOUT_MS)
        task = asyncio.create_task(service.watchdog())
        try:
            await asyncio.sleep(0.03)
            self.assertEqual(service.controller.outputs, (0, 0))
        finally:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task


if __name__ == "__main__":
    unittest.main()
