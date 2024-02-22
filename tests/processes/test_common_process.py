import pytest

from typing import Dict
from sentinel.processes.common import Process


def test_common_process_init():
    '''
    Test | Common Process | Init
    '''
    proc = Process(name='TestProccess', description='Test Process', 
                   parameters={}, inputs={}, outputs={}, databases={})
    assert isinstance(proc, Process), "Incorrect process type"


@pytest.mark.asyncio
async def test_common_process_custom_init():
    '''
    Test | Common Process | Custom Initialization
    '''
    class CustomProcess(Process):
        async def init(self) -> None:
            self.default_balance = self.parameters.get('default_balance', 10)

    proc = CustomProcess(name='TestProccess', 
                        description='Test Process', 
                        parameters={
                            'default_balance': 100
                        }, 
                        inputs={}, outputs={}, databases={})
    await proc.init()
    assert proc.default_balance == 100, "Incorrect default balance value"