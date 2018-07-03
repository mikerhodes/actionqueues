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
exception.

```python
import random
from actionqueues import actionqueue, action

class MyAction(action.Action):

    def __init__(self):
        self._value = 0

    def execute(self):
        """Called if actions before it in the queue complete successfully.

        Raise any exception to indicate failure.
        """
        self._value = 1
        if random.choice([True, False]):
            raise Exception()

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
