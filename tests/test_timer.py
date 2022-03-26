import pytest
from time import time
from timers import DelayTimer, FREQ


def test_delay_timer():
    t = DelayTimer()

    #test getting timer value before its set
    with pytest.raises(Exception):
        t.get()

    t.set(256)
    curr_time= time()

    while t.get() > 0:
        pass

    time_passed = time() - curr_time
    assert time_passed >= 256/FREQ
    assert time_passed <= 316/FREQ # 1 sec difference as marjin
