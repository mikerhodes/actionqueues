"""Simple state machine to manage restrictions on action queue calls."""

from enum import Enum

class AQStateMachineStates(Enum):
    """States for state machine."""
    init = 0
    add = 1
    execute = 2
    rollback = 3
    execute_complete = 4
    rollback_complate = 5

class AQStateMachine(object):
    """This class encodes the transitions that ActionQueues are allowed to do,
    following these rules:

    1. One or more calls to ADD
    2. One call to Execute
    3. One call to Rollback

    This allows for executing a full rollback on successful complete, but
    you can't call execute or rollback twice.

    INIT
     |
     | <-\
     v   |
    ADD -/
     |
     V
    EXECUTE -> EXECUTE_COMPLETE
     |           |
     v           |
    ROLLBACK  <--/
     |
     v
    ROLLBACK_COMPLETE
    """

    def __init__(self):
        self.state = AQStateMachineStates.init

    def transition_to_add(self):
        """Transition to add"""
        assert self.state in [AQStateMachineStates.init, AQStateMachineStates.add]
        self.state = AQStateMachineStates.add

    def transition_to_execute(self):
        """Transition to execute"""
        assert self.state in [AQStateMachineStates.add]
        self.state = AQStateMachineStates.execute

    def transition_to_rollback(self):
        """Transition to rollback"""
        assert self.state in [AQStateMachineStates.execute, AQStateMachineStates.execute_complete]
        self.state = AQStateMachineStates.rollback

    def transition_to_execute_complete(self):
        """Transition to execute complate"""
        assert self.state in [AQStateMachineStates.execute]
        self.state = AQStateMachineStates.execute_complete

    def transition_to_rollback_complete(self):
        """Transition to rollback complete"""
        assert self.state in [AQStateMachineStates.rollback]
        self.state = AQStateMachineStates.rollback_complate
