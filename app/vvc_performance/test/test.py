import unittest
from ..src.common.vvc_exec import vvc_executer

class ExecuterTest(unittest.TestCase):
    def __init__(self, methodName: str = "test_vvc_executer") -> None:
        self._exec = vvc_executer()
        super().__init__(methodName)

    def test(self):
        self._exec.run_exec()
        

