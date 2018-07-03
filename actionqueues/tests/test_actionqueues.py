import pytest

from actionqueues import actionqueue
from actionqueues import action

class MockCommand(action.Action):

    def __init__(self, execute_state, rollback_state):
        self._execute_called = False
        self._rollback_called = False
        self._execute_state = execute_state
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

class State(object):
    """The state object maintains a simple counter that allows
    us to check Actions are executed in order."""

    def __init__(self):
        self._counter = 0

    def inc(self):
        self._counter += 1
        return self._counter

def test_execute_actions():
    exec_state = State()
    rollback_state = State()
    actions = [
        MockCommand(exec_state, rollback_state),
        MockCommand(exec_state, rollback_state)
    ]
    q = actionqueue.ActionQueue()
    for action in actions:
        q.add(action)
    q.execute()

    # Ensure executes have been run, and in correct order
    for idx,action in enumerate(actions):
        assert action._execute_called
        assert action._execute_value == idx+1

def test_rollback_actions():
    exec_state = State()
    rollback_state = State()
    actions = [
        MockCommand(exec_state, rollback_state),
        MockCommand(exec_state, rollback_state)
    ]
    q = actionqueue.ActionQueue()
    for action in actions:
        q.add(action)
    q.execute()
    q.rollback()

    # Ensure rollbacks have been run, and in correct order
    for idx,action in enumerate(reversed(actions)):
        assert action._rollback_called
        assert action._rollback_value == idx+1

def test_explode_action():
    exec_state = State()
    rollback_state = State()
    actions = [
        MockCommand(exec_state, rollback_state),
        MockCommand(exec_state, rollback_state),
        ExplodingCommand(),
        MockCommand(exec_state, rollback_state)
    ]
    q = actionqueue.ActionQueue()
    for action in actions:
        q.add(action)

    try:
        q.execute()
    except:
        pass  # expected due to ExplodingCommand

    assert actions[0]._execute_called
    assert actions[1]._execute_called
    assert actions[2]._execute_called
    assert not actions[3]._execute_called

    q.rollback()

    assert actions[0]._rollback_called
    assert actions[0]._rollback_value == 2
    assert actions[1]._rollback_called
    assert actions[1]._rollback_value == 1
    assert actions[2]._rollback_called
    assert not actions[3]._rollback_called



