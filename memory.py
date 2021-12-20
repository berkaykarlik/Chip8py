import numpy as np


class Memory():

    def __init__(self) -> None:
        self.__memory = np.zeros(0x1000, np.uint8)
        self.__pc = 0x200
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

    def get_mem(self, addr: int) -> np.uint8:
        """returns the value from the memory cell of the address provided"""
        if addr < 0x200 or addr > 0xFFF:
            raise IndexError
        return self.__memory[addr]

    def set_mem(self, addr: int, value: int) -> None:
        """sets the provided value to the memory cell of the address provied"""
        if self.__pc > 0xFFF:
            raise MemoryError
        self.__memory[addr] = value

    def load_instr(self, value: int) -> None:
        """load instrunctions to memory at start"""
        if self.instr_ptr > 0xFFF:
            raise MemoryError
        self.__memory[self.instr_ptr:self.instr_ptr +
                      2] = np.frombuffer(value, dtype=np.uint8)
        self.instr_ptr += 0x2

    def fetch(self) -> bytes:
        """get the next instructions pc is pointing to"""
        instr = self.__memory[self.__pc:self.__pc+2].tobytes()
        self.__pc += 0x2
        return instr

    def jump(self, addr: int) -> None:
        """move the pc to given address"""
        if addr < 0x200 or addr > 0xFFF:
            raise IndexError
        self.set_pc(addr)

    def skip(self) -> None:
        self.pc += 0x2

    def get_pc(self) -> int:
        return self.__pc

    def set_pc(self, addr: int) -> None:
        """set pc to given address value if within memory limits"""
        if addr < 0x200 or addr > 0xFFF:
            raise IndexError
        self.__pc = addr


if __name__ == '__main__':
    mem = Memory()
    print(mem._Memory__memory[0x50:0xA0])
