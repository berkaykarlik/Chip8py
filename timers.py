from time import time
from threading import Timer
FREQ = 60  # hz
DELAY_LIMIT = 256  # 1 byte


class DelayTimer():
    def __init__(self) -> None:
        self.__value = 0
        pass

    def __decrement():
        pass

    def delay(self, delay_value):
        self.__value = delay_value % DELAY_LIMIT


class SoundTimer():
    def __init__(self) -> None:
        pass
