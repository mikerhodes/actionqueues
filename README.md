# Action Queues

`actionqueues` is a lightweight way to queue up commands for execution and
rollback on failures.

## Installing

```
pip install actionqueues
```

(later anyway)

## Using Action Queues

It's barebones, the main point is to provide a framework to work within for
actions that have side effects. It's basically the Command pattern, with a
tiny execution framework.

An `ActionQueue` holds `Actions` for execution and rollback. Add `Action` objects
to an `ActionQueue`. Call `ActionQueue#execute` to run the actions in the order
added to the `ActionQueue`. If an `Action` raises an exception, this is propagated
back up to the caller. Catch it and call `ActionQueue#rollback` to call rollback
on the `Actions` that have been executed, including the one that raised the
exception. Rollback will not be called on actions where `execute` has not been
called.

If the `execute` method of an action encounters a problem that may be fixed
by retrying, it should raise a `actionqueue.RetryActionException`, which
takes an optional `ms_backoff` argument to specify a time to sleep. The
`ActionQueue` will retry as long as the action keeps raising
`actionqueue.RetryActionException`, so the action must maintain a retry count
to avoid endless retries.

```python
import random
from actionqueues import actionqueue, action

SUCCEED = 0
RETRY = 1
FAIL = 2

class MyAction(action.Action):

    def __init__(self):
        self._value = 0

    def execute(self):
        """Called if actions before it in the queue complete successfully.

        Raise any exception to indicate failure.
        """
        self._value = 1
        action = random.choice([SUCCEED, RETRY, FAIL])
        if action == RETRY:
            raise actionqueue.RetryActionException(ms_backoff=0)
        elif action == FAIL:
            raise Exception()
        # otherwise succeed

    def rollback(self):
        """Called in reverse order for all actions queued whose execute
        method was called when the ActionQueue's rollback method is called.
        """
        if self._value = 1:
            self._value = 0

q = actionqueue.ActionQueue()
q.add(MyAction())
q.add(MyAction())

try:
    q.execute()
except:
    q.rollback()
```
