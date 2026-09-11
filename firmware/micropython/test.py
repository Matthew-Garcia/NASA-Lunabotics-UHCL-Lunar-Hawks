"""Portable dry-run logic checks. No network, GPIO, or motor outputs."""
from dry_run import DryRunController, TIMEOUT_MS, mix, parse_command


def run():
    assert mix(1.0, 0.0) == (1.0, 1.0)
    assert mix(0.0, 1.0) == (-1.0, 1.0)
    assert mix(1.0, 1.0) == (0.0, 1.0)
    assert parse_command('{"v":1,"w":0,"deadman":false}') == (0.0, 0.0)
    controller = DryRunController()
    controller.receive('{"v":0.5,"w":0,"deadman":true}', 100)
    assert controller.expire(100 + TIMEOUT_MS - 1) == (0.5, 0.5)
    assert controller.expire(100 + TIMEOUT_MS) == (0.0, 0.0)
    for bad in ('{}', '[]', 'invalid', '{"v":2,"w":0,"deadman":true}',
                '{"v":true,"w":0,"deadman":true}',
                '{"v":0,"w":0,"deadman":1}',
                '{"v":1e999,"w":0,"deadman":true}'):
        controller.receive('{"v":1,"w":0,"deadman":true}', 1)
        try:
            controller.receive(bad, 2)
        except (ValueError, TypeError, OverflowError):
            assert controller.outputs == (0.0, 0.0)
        else:
            raise AssertionError("Accepted invalid payload")
    print("PASS: dry-run mixer, validation, deadman, timeout, malformed-input stop")


if __name__ == "__main__":
    run()
