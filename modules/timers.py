from time import time, sleep
from threading import Timer
from array import array
import pygame
from pygame.mixer import Sound, get_init, pre_init


FREQ = 60  # hz
DELAY_LIMIT = 256  # 1 byte


class DelayTimer():
    def __init__(self) -> None:
        self.__value = 0.0
        self.__time  = 0.0
        pass


    def set(self, value: int) -> None:
        if value.bit_length() > DELAY_LIMIT:
            raise TypeError("1 byte max")
        self.__value = value
        self.__time = time()


    def get(self) -> int:
        """calculate how much time passed since last set and return decremented value"""
        time_passed = time() - self.__time
        self.__time = time()
        self.__value = self.__value - (time_passed * FREQ)

        if self.__value <= 0:
            self.__value = 0

        return int(self.__value)


class SoundTimer(Sound):
    def __init__(self,frequency=440, volume=.1) -> None:
        pygame.init()
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)
        pre_init(44100, -16, 1, 1024)


    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


    def set(self, value: int) -> None:
        duration_ms = int(1000* value / FREQ )
        self.play(-1,duration_ms)


if __name__ == "__main__":
    pygame.init()
    SoundTimer(440).play(-1)
    sleep(5)