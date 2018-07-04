
"""A set of mock commands that allow controlling their execution and
that record what has happened to them.
"""

from actionqueues import action
from actionqueues import actionqueue

class MockCommand(action.Action):
    """Simply records that execute/rollback were called and the value from
    the State objects passed in at that time.
    """

    def __init__(self, execute_state, rollback_state):
        self._execute_called = False
        self._execute_state = execute_state
        self._rollback_called = False
        self._rollback_state = rollback_state

    def execute(self):
        self._execute_called = True
        self._execute_value = self._execute_state.inc()

    def rollback(self):
        self._rollback_called = True
        self._rollback_value = self._rollback_state.inc()

class ExplodingCommand(action.Action):

    def __init__(self):
        self._execute_called = False
        self._rollback_called = False

    def execute(self):
        self._execute_called = True
        raise IOError()

    def rollback(self):
        self._rollback_called = True

class RetryCommand(action.Action):
    """Command that fails with retry exception a certain number of times,
    then succeeds.
    """

    def __init__(self, execute_state, failures, delay_ms=0):
        self._failures = failures
        self._execute_called = False
        self._execute_state = execute_state
        self._delay_ms = delay_ms

    def execute(self):
        self._execute_called = True
        self._execute_value = self._execute_state.inc()
        self._failures -= 1
        if self._failures >= 0:
            raise actionqueue.ActionRetryException(self._delay_ms)

class RetryThenExplodeCommand(action.Action):
    """Command that fails with retry exception a certain number of times,
    then fails with a non-retry exception.
    """

    def __init__(self, execute_state, failures, delay_ms=0):
        self._failures = failures
        self._execute_called = False
        self._execute_state = execute_state
        self._delay_ms = delay_ms
        self._rollback_called = False

    def execute(self):
        self._execute_called = True
        self._execute_value = self._execute_state.inc()
        self._failures -= 1
        if self._failures >= 0:
            raise actionqueue.ActionRetryException(ms_backoff=self._delay_ms)
        else:
            raise Exception()

    def rollback(self):
        self._rollback_called = True

class State(object):
    """The state object maintains a simple counter that allows
    us to check Actions are executed in order. A State object is
    shared between multiple mock actions so that the number of
    calls of each action can be recorded and the order in which
    they were called."""

    def __init__(self):
        self._counter = 0

    def inc(self):
        self._counter += 1
        return self._counter
