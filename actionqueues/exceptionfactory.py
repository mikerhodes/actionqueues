
from actionqueues.actionqueue import ActionRetryException

class DoublingBackoffExceptionFactory(object):
    """Raise a retry exception a number of times, then fail with either
    a user-provided exception or a generic exception.
    """

    def __init__(self, retries=3, ms_backoff_initial=500):
        """Initialise the factory with a number of retries and an initial
        backoff.
        """
        self._max_retries = retries
        self._executed_retries = 0
        self._ms_backoff = ms_backoff_initial

    def raise_exception(self, original_exception=None):
        """Raise a retry exception if under the max retries. After, raise the
        original_exception provided to this method or a generic Exception if
        none provided.
        """
        if self._executed_retries < self._max_retries:
            curr_backoff = self._ms_backoff
            self._executed_retries += 1
            self._ms_backoff = self._ms_backoff * 2
            raise ActionRetryException(curr_backoff)
        else:
            raise original_exception or Exception()
