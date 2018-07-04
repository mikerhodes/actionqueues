import time

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

    def add(self, action):
        self._actions.append(action)

    def execute(self):
        """Execute all actions, throwing an ExecutionException on failure.

        Catch the ExecutionException and call rollback() to rollback.
        """
        for action in self._actions:
            self._executed_actions.append(action)
            self.execute_with_retries(action, lambda a: a.execute())

    def rollback(self):
        for action in reversed(self._executed_actions):
            try:
                self.execute_with_retries(action, lambda a: a.rollback())
            except:
                pass  # on exception, carry on with rollback of other steps

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
            except ActionRetryException, ex:  # other exceptions should bubble out
                retry = True
                time.sleep(ex.ms_backoff / 1000.0)


