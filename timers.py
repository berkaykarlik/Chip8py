from time import time
from threading import Timer

FREQ = 60  # hz
DELAY_LIMIT = 256  # 1 byte


class DelayTimer():
    def __init__(self) -> None:
        self.__value = 0
        self.__time = None
        pass


    def set(self, value: int) -> None:
        if value.bit_length() > DELAY_LIMIT:
            raise TypeError("1 byte max")
        self.__value = value
        self.__time = time()


    def get(self) -> None:
        """calculate how much time passed since last set and return decremented value"""
        if self.__time is None:
            raise Exception("Timer not set")
        else:
            time_passed = time() - self.__time
            self.__time = time()
            self.__value = self.__value - (time_passed * FREQ)

            if self.__value <= 0:
                self.__time = None
                self.__value = 0

            return self.__value


class SoundTimer():  # TODO:beep somehow
    def __init__(self) -> None:
        pass

    def set(self, value: int) -> None:
        self.__value = value
        Timer(1/60, self.decrement).start()

    def decrement(self) -> None:
        if self.__value > 0:
            self.__value -= 1
            Timer(1/60, self.decrement).start()


