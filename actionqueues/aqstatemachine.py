"""Simple state machine to manage restrictions on action queue calls."""

AQStateMachine_INIT = 0
AQStateMachine_ADD = 1
AQStateMachine_EXECUTE = 2
AQStateMachine_ROLLBACK = 3
AQStateMachine_EXECUTE_COMPLETE = 4
AQStateMachine_ROLLBACK_COMPLETE = 5

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
        self.state = AQStateMachine_INIT

    def transition_to_add(self):
        assert self.state in [AQStateMachine_INIT, AQStateMachine_ADD]
        self.state = AQStateMachine_ADD

    def transition_to_execute(self):
        assert self.state in [AQStateMachine_ADD]
        self.state = AQStateMachine_EXECUTE

    def transition_to_rollback(self):
        assert self.state in [AQStateMachine_EXECUTE, AQStateMachine_EXECUTE_COMPLETE]
        self.state = AQStateMachine_ROLLBACK

    def transition_to_execute_complete(self):
        assert self.state in [AQStateMachine_EXECUTE]
        self.state = AQStateMachine_EXECUTE_COMPLETE

    def transition_to_rollback_complete(self):
        assert self.state in [AQStateMachine_ROLLBACK]
        self.state = AQStateMachine_ROLLBACK_COMPLETE
