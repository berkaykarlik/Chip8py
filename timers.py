import time
from threading import Timer

FREQ = 60  # hz
DELAY_LIMIT = 256  # 1 byte


class DelayTimer():
    def __init__(self) -> None:
        self.__value = 0
        pass

    def set(self, value: int) -> None:
        self.__value = value
        Timer(1/60, self.decrement).start()

    def get(self) -> None:
        return self.__value

    def decrement(self) -> None:
        if self.__value > 0:
            self.__value -= 1
            Timer(1/60, self.decrement).start()


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


if __name__ == '__main__':
    t = DelayTimer()
    t.set(60)

    while t.get() != 0:
        print(t.get())
