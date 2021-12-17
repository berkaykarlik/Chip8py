import numpy as np


class Memory():

    def __init__(self) -> None:
        self.__memory = np.zeros(0x1000, np.uint8)
        self.pc = 0x200
        self.instr_ptr = 0x200
        self.i = None
        # add font
        self.__memory[0x50:0xA0] = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
                                    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                                    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
                                    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
                                    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
                                    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
                                    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
                                    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
                                    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
                                    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
                                    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
                                    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
                                    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
                                    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
                                    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
                                    0xF0, 0x80, 0xF0, 0x80, 0x80]  # F

    def get(self, memory_address):
        return self.__memory[memory_address]

    def set(self, memory_address, value):
        if self.pc > 0xFFF:
            raise MemoryError
        self.__memory[memory_address] = value

    def load_instr(self, value):
        if self.instr_ptr > 0xFFF:
            raise MemoryError
        self.__memory[self.instr_ptr:self.instr_ptr +
                      2] = int.from_bytes(value, 'big', signed=False)
        self.instr_ptr += 0x2


if __name__ == '__main__':
    mem = Memory()
    print(mem._Memory__memory[0x50:0xA0])
