from time import sleep
FREQ = 60  # hz
DELAY_LIMIT = 256  # 1 byte


class DelayTimer():
    def __init__(self) -> None:
        self.__value = 0
        pass

    def delay(self, delay_value):
        self.__value = delay_value % DELAY_LIMIT
        while self.__value > 0:
            sleep(1/60)
            self.__value -= 1


class SoundTimer():
    def __init__(self) -> None:
        pass


if __name__ == '__main__':
    DelayTimer().delay(60)
