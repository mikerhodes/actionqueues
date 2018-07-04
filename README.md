# Action Queues

`actionqueues` is a lightweight way to queue up commands for execution and
rollback on failures.

The idea is that it provides a framework for safely
executing sequences of action with side-effects, like database writes, that
might need later rolling back if later actions fail. In addition, it provides
a standardised way for actions to be retried.

For example, a user sign up process may write to several different systems.
If one system is down, then the other systems modified so far need cleaning
up before the failure is propagated back to the user. Using `actionqueues`
with an action for each external system to be modified enables this pattern,
along with simple retry semantics for likely-transient failures such as network
blips.

## Installing

```
pip install actionqueues
```

(Later anyway, still need to figure pypi management!)

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

    def __init__(self, id):
        self._id = id
        self._value = 0

    def execute(self):
        """Called if actions before it in the queue complete successfully.

        Raise any exception to indicate failure.
        """
        action = random.choice([SUCCEED, RETRY, FAIL])
        if action == RETRY:
            print self._id, "Throwing retry exception"
            raise actionqueue.ActionRetryException(ms_backoff=0)
        elif action == FAIL:
            print self._id, "Throwing failure exception"
            raise Exception()
        else:
            print self._id, "Executing success action"
            self._value = 1


    def rollback(self):
        """Called in reverse order for all actions queued whose execute
        method was called when the ActionQueue's rollback method is called.
        """
        print self._id, "Rolling back action"
        if self._value == 1:
            self._value = 0

q = actionqueue.ActionQueue()
q.add(MyAction("a"))
q.add(MyAction("b"))

try:
    q.execute()
except:
    q.rollback()
```

## Retry exception helpers

It can be tedious to keep track of the backoff and retry count for an action.
Therefore `actionqueues` provides helpers for this called exception factories.
These are created when the `Action` is initialised, and when an `execute`
method hits a retriable exception, it calls the factory's `raise_exception()`
method. In general, this will throw `ActionRetryException` exceptions for a
given number of retries, then throw a generic exception, or one provided by
the `Action` object.

The available exception factories are:

- `DoublingBackoffExceptionFactory` which will throw a configurable number
    `ActionRetryException` exceptions, each doubling its backoff time.

In this example, the `ZeroDivisionError` will cause 5 retries, at 100, 200,
400, 800 and 1600ms delays:

```python
from actionqueues import actionqueue, action
from actionqueues.exceptionfactory import DoublingBackoffExceptionFactory

class MyFailingAction(action.Action):

    def __init__(self):
        self._run = 1
        self._ex_factory = DoublingBackoffExceptionFactory(
            retries=5,
            ms_backoff_initial=100
        )

    def execute(self):
        """Execute an always failing action, but have it retried 5 times."""
        print "Executing action", self._run
        self._run += 1
        try:
            1 / 0
        except ZeroDivisionError, ex:
            self._ex_factory.raise_exception(original_exception=ex)

q = actionqueue.ActionQueue()
q.add(MyFailingAction())

try:
    q.execute()
except:
    print "boom"
```
