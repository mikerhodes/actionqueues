import time

from actionqueues.aqstatemachine import AQStateMachine

class ActionRetryException(Exception):
    """Exception thrown by actions when they should be retried."""
    def __init__(self, ms_backoff=0):
        """Initialise with a backoff time."""
        self.ms_backoff = ms_backoff

class ActionQueue(object):
    """Queue of Action objects ready for execution."""

    def __init__(self):
        self._actions = list()
        self._executed_actions = list()
        self._state_machine = AQStateMachine()

    def add(self, action):
        self._state_machine.transition_to_add()
        self._actions.append(action)

    def execute(self):
        """Execute all actions, throwing an ExecutionException on failure.

        Catch the ExecutionException and call rollback() to rollback.
        """
        self._state_machine.transition_to_execute()
        for action in self._actions:
            self._executed_actions.append(action)
            self.execute_with_retries(action, lambda a: a.execute())
        self._state_machine.transition_to_execute_complete()

    def rollback(self):
        self._state_machine.transition_to_rollback()
        for action in reversed(self._executed_actions):
            try:
                self.execute_with_retries(action, lambda a: a.rollback())
            except:
                pass  # on exception, carry on with rollback of other steps
        self._state_machine.transition_to_rollback_complete()

    def execute_with_retries(self, action, f):
        """Execute function f with single argument action. Retry if
        ActionRetryException is raised.
        """
        # Run action until either it succeeds or throws an exception
        # that's not an ActionRetryException
        retry = True
        while retry:
            retry = False
            try:
                f(action)
            except ActionRetryException as ex:  # other exceptions should bubble out
                retry = True
                time.sleep(ex.ms_backoff / 1000.0)


