import pygame
import numpy as np
from time import sleep


class Display():
    HEIGHT = 32
    WIDTH = 64

    def __init__(self) -> None:
        self.__frame = np.ones(
            (Display.WIDTH, Display.HEIGHT), np.uint8) * 255

        # Original chip-8 is 64x32, its too small for computer screen
        display_width = Display.WIDTH * 10 * 2
        display_height = Display.HEIGHT * 10 * 2
        self.display_size = (display_width, display_height)

        pygame.init()
        pygame.display.set_caption("CHIP-8")
        self.__display = pygame.display.set_mode(self.display_size)

    def update_display(self):
        surf = pygame.surfarray.make_surface(self.__frame)
        surf = pygame.transform.scale(surf, self.display_size)
        self.__display.blit(surf, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    display = Display()
    # test if we can update display, spoilers we can
    while(True):
        display._Display__frame = display._Display__frame / \
            255 if display._Display__frame.any() == 255 else display._Display__frame * 255
        display.update_display()
        sleep(1)
