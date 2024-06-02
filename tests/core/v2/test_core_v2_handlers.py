from sentinel.core.v2.handler import FlowType, Handler


def test_core_handler_init():
    handler = Handler(id="base/handler", flow_type=FlowType.inbound)
    assert isinstance(handler, Handler), "Incorrect handler type"
    assert handler.name == "BaseHandler", "Incorrect handler name"

    handler = Handler(id="base/handler", flow_type=FlowType.inbound, name="TestHandler")
    assert handler.name == "TestHandler", "Incorrect handler name"
