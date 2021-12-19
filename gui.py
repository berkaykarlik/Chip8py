import pygame
import numpy as np


class Gui():
    HEIGHT = 32
    WIDTH = 64
    ALLOWED_KEYS = {"1", "2", "3", "4",
                    "q", "w", "e", "r",
                    "a", "s", "d", "f",
                    "z", "x", "c", "v"}

    def __init__(self) -> None:
        self.__frame = np.zeros(
            (Gui.WIDTH, Gui.HEIGHT), np.uint8)

        # Original chip-8 is 64x32, its too small for computer screen
        display_width = Gui.WIDTH * 10 * 2
        display_height = Gui.HEIGHT * 10 * 2
        self.display_size = (display_width, display_height)

        pygame.init()
        pygame.display.set_caption("CHIP-8")
        self.__display = pygame.display.set_mode(self.display_size)

    def update_display(self):
        surf = pygame.surfarray.make_surface(self.__frame)
        surf = pygame.transform.scale(surf, self.display_size)
        self.__display.blit(surf, (0, 0))
        pygame.display.update()

    def process_events(self):
        events = pygame.event.get()
        pressed_keys = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key)
                if key_pressed in Gui.ALLOWED_KEYS:
                    pressed_keys.append(key_pressed)
        return pressed_keys

    def clear_screen(self):
        self.__frame.fill(0)
        self.update_display()


if __name__ == '__main__':
    display = Gui()
    # test if we can update display, spoilers we can
    while(True):
        # stroke warning, fast changing color ahead
        keys_pressed = display.process_events()
        if keys_pressed:
            print(keys_pressed)
