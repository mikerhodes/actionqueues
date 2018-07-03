
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
            action.execute()

    def rollback(self):
        for action in reversed(self._executed_actions):
            action.rollback()
