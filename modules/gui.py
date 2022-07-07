import pygame
import numpy as np


class Gui():
    HEIGHT = 32
    WIDTH = 64
    ALLOWED_KEYS = {"1", "2", "3", "4",
                    "q", "w", "e", "r",
                    "a", "s", "d", "f",
                    "z", "x", "c", "v"}
    KEY_MAPPING = {"1": 0x1, "2": 0x2, "3": 0x3, "4": 0xC,
                   "q": 0x4, "w": 0x5, "e": 0x6, "r": 0xD,
                   "a": 0x7, "s": 0x8, "d": 0x9, "f": 0xE,
                   "z": 0xA, "x": 0x0, "c": 0xB, "v": 0xF}

    def __init__(self) -> None:
        self.__frame = np.zeros((Gui.WIDTH, Gui.HEIGHT), np.uint8)

        # Original chip-8 is 64x32, its too small for computer screen
        display_width = Gui.WIDTH * 10 * 2
        display_height = Gui.HEIGHT * 10 * 2
        self.display_size = (display_width, display_height)

        pygame.init()
        pygame.display.set_caption("CHIP-8")
        self.__display = pygame.display.set_mode(self.display_size)
        self.pool : set = set()

    def update_display(self):
        surf = pygame.surfarray.make_surface(self.__frame*255)
        surf = pygame.transform.scale(surf, self.display_size)
        self.__display.blit(surf, (0, 0))
        pygame.display.update()

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key)
                if key_pressed in Gui.ALLOWED_KEYS:
                    self.pool.add(Gui.KEY_MAPPING[key_pressed])
            if event.type == pygame.KEYUP:
                key_pressed = pygame.key.name(event.key)
                self.pool.remove(Gui.KEY_MAPPING[key_pressed])


    def get_press_release(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYUP:
                key_pressed = pygame.key.name(event.key)
                return Gui.KEY_MAPPING[key_pressed]

    def get_pool(self):
        return list(self.pool)

    def clear_screen(self):
        self.__frame.fill(0)
        self.update_display()

    def set(self, x:int, y:int, bit_val:int) -> bool:
        # x = x % Gui.WIDTH
        # y = y % Gui.HEIGHT
        if x >= Gui.WIDTH or y >= Gui.HEIGHT:
            return False
        prev = int(self.__frame[x][y])
        self.__frame[x][y] = prev ^ bit_val
        return prev & bit_val

    def draw_test(self):
        self.__frame[:, 1] = np.ones((1, Gui.WIDTH), np.uint8) * 255


if __name__ == '__main__':
    display = Gui()
    # test if we can update display, spoilers we can
    while True:
        display.process_events()
        keys = display.get_pool()
        if keys:
            print(keys)
