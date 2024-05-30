from sentinel.core.v2.handler import Handler


def test_core_handler_init():
    handler = Handler()
    assert isinstance(handler, Handler), "Incorrect handler type"
