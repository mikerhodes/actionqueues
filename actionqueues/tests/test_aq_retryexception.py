from datetime import datetime

from actionqueues import actionqueue
from .mock_actions import *

def test_retry_succeed_action():
    exec_state = State()
    rollback_state = State()
    actions = [
        MockCommand(exec_state, rollback_state),
        MockCommand(exec_state, rollback_state),
        RetryCommand(exec_state, 5),
        MockCommand(exec_state, rollback_state)
    ]
    q = actionqueue.ActionQueue()
    for action in actions:
        q.add(action)

    q.execute()

    assert actions[0]._execute_called
    assert actions[0]._execute_value == 1
    assert actions[1]._execute_called
    assert actions[1]._execute_value == 2
    assert actions[2]._execute_called
    assert actions[2]._execute_value == 8  # i.e., execute called 6 times (5 failures, 1 success)
    assert actions[3]._execute_called
    assert actions[3]._execute_value == 9

def test_retry_explode_action():
    exec_state = State()
    rollback_state = State()
    actions = [
        MockCommand(exec_state, rollback_state),
        MockCommand(exec_state, rollback_state),
        RetryThenExplodeCommand(exec_state, 5),
        MockCommand(exec_state, rollback_state)
    ]
    q = actionqueue.ActionQueue()
    for action in actions:
        q.add(action)

    try:
        q.execute()
    except:
        pass  # expected from RetryThenExplodeCommand

    assert actions[0]._execute_called
    assert actions[0]._execute_value == 1
    assert actions[1]._execute_called
    assert actions[1]._execute_value == 2
    assert actions[2]._execute_called
    assert actions[2]._execute_value == 8  # i.e., execute called 6 times (5 failures, 1 success)
    assert not actions[3]._execute_called

    q.rollback()

    assert actions[0]._rollback_called
    assert actions[0]._rollback_value == 2
    assert actions[1]._rollback_called
    assert actions[1]._rollback_value == 1
    assert actions[2]._rollback_called
    assert not actions[3]._rollback_called

def test_retry_delay():

    FAILURES = 5
    DELAY = 50
    expected_delay_at_least = ((FAILURES*DELAY) / 1000.0)

    exec_state = State()
    rollback_state = State()
    actions = [
        MockCommand(exec_state, rollback_state),
        MockCommand(exec_state, rollback_state),
        RetryCommand(exec_state, FAILURES, DELAY),  # introduce 50ms delay
        MockCommand(exec_state, rollback_state)
    ]
    q = actionqueue.ActionQueue()
    for action in actions:
        q.add(action)

    start = datetime.now()
    q.execute()
    end = datetime.now()

    assert (end - start).total_seconds() > expected_delay_at_least
