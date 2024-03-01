import pytest

from sentinel.processes.common import Process

@pytest.mark.asyncio
async def test_process_channels_init():
    """ 
    Test | Process | Channels Init
    """
    class CustomProcess(Process):
        pass

    proc = CustomProcess(
        name="TestProccess",
        description="Test Process",
        parameters={"default_balance": 100},
        inputs={},
        outputs={},
        databases={},
    )

    assert isinstance(proc, CustomProcess), "Incorrect process type"
