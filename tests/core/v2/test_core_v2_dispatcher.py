from sentinel.core.v2.dispatcher import Dispatcher
from sentinel.models.settings import Settings


def test_core_dispatcher():
    dispatcher = Dispatcher(settings=Settings())
    assert isinstance(dispatcher, Dispatcher), "Incorrect dispatcher type"
