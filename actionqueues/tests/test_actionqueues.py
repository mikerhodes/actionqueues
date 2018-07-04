from actionqueues import actionqueue
from .mock_actions import *

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



