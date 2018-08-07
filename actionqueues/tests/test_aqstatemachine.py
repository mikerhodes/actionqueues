# pylint: disable=invalid-name,missing-docstring

import pytest

from actionqueues.aqstatemachine import AQStateMachine

def test_valid_sequence():
    m = AQStateMachine()
    m.transition_to_add()
    m.transition_to_add()
    m.transition_to_execute()
    m.transition_to_rollback()
    m.transition_to_rollback_complete()

def test_invalid_sequence_1():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_execute()

def test_invalid_sequence_2():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_rollback()

def test_invalid_sequence_3():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_execute_complete()

def test_invalid_sequence_4():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_rollback_complete()

def test_invalid_sequence_5():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_add()
        m.transition_to_execute()
        m.transition_to_rollback_complete()

def test_invalid_sequence_6():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_add()
        m.transition_to_execute()
        m.transition_to_execute_complete()
        m.transition_to_rollback_complete()

def test_invalid_sequence_7():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_add()
        m.transition_to_execute()
        m.transition_to_execute()

def test_invalid_sequence_8():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_add()
        m.transition_to_execute()
        m.transition_to_rollback()
        m.transition_to_rollback()

def test_invalid_sequence_9():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_add()
        m.transition_to_execute()
        m.transition_to_execute_complete()
        m.transition_to_execute()

def test_invalid_sequence_10():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_add()
        m.transition_to_execute_complete()

def test_invalid_sequence_11():
    m = AQStateMachine()
    with pytest.raises(AssertionError):
        m.transition_to_add()
        m.transition_to_rollback_complete()
