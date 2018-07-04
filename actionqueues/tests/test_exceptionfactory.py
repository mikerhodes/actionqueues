import pytest

from actionqueues.exceptionfactory import DoublingBackoffExceptionFactory
from actionqueues.actionqueue import ActionRetryException

def test_DoublingBackoffExceptionFactory_defaults():
    ex_factory = DoublingBackoffExceptionFactory()

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.value.ms_backoff == 500

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.value.ms_backoff == 1000

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.value.ms_backoff == 2000

    with pytest.raises(Exception) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.type != ActionRetryException

    with pytest.raises(Exception) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.type != ActionRetryException


def test_DoublingBackoffExceptionFactory_custom():

    ex_factory = DoublingBackoffExceptionFactory(retries=4, ms_backoff_initial=100)

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.value.ms_backoff == 100

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.value.ms_backoff == 200

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.value.ms_backoff == 400

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.value.ms_backoff == 800

    with pytest.raises(Exception) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.type != ActionRetryException

    with pytest.raises(Exception) as excinfo:
        ex_factory.raise_exception()
    assert excinfo.type != ActionRetryException

def test_DoublingBackoffExceptionFactory_raise_original_exception():

    ex_factory = DoublingBackoffExceptionFactory(retries=1, ms_backoff_initial=100)

    original_exception = IOError()
    original_exception2 = ZeroDivisionError()

    with pytest.raises(ActionRetryException) as excinfo:
        ex_factory.raise_exception(original_exception=original_exception)
    assert excinfo.value.ms_backoff == 100

    with pytest.raises(Exception) as excinfo:
        ex_factory.raise_exception(original_exception=original_exception)
    assert excinfo.value == original_exception

    with pytest.raises(Exception) as excinfo:
        ex_factory.raise_exception(original_exception=original_exception2)
    assert excinfo.value == original_exception2
