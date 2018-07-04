
class Action(object):

    def execute(self):
        """Execute this action.

        Save state on the object to allow for rollback of side-effects.

        Throw a ActionRetryException if a failure should be retried later.
        """
        pass

    def rollback(self):
        """Rollback the side-effects of the action.

        This will be called if a later action in the queue fails to execute,
        or this action itself throws an exception.
        """
        pass
