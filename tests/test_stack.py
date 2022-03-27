import pytest
from modules.stack import Stack


def test_push_pop():
    stack = Stack()
    stack.push(0xFF)
    assert stack.pop() == 0xFF

def test_stack_limit():
    stack = Stack()
    for i in range(16):
        stack.push(i)

    stack.push(i+1)

    # test pop afterwards for all values pushed
    for i in range(17):
        assert stack.pop() == 16 - i