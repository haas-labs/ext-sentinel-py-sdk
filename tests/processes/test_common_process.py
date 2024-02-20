from typing import Dict
from sentinel.processes.common import Process


def test_common_process_init():
    '''
    Test | Common Process | Init
    '''
    proc = Process(name='TestProccess', description='Test Process', 
                   parameters={}, inputs={}, outputs={}, databases={})
    assert isinstance(proc, Process), "Incorrect process type"


def test_common_process_custom_init():
    '''
    Test | Common Process | Custom Initialization
    '''
    class CustomProcess(Process):
        def init(self, parameters: Dict) -> None:
            self.default_balance = parameters.get('default_balance', 10)

    proc = CustomProcess(name='TestProccess', 
                        description='Test Process', 
                        parameters={
                            'default_balance': 100
                        }, 
                        inputs={}, outputs={}, databases={})
    assert proc.default_balance == 100, "Incorrect default balance value"