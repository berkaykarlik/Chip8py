import numpy as np


class Register():
    def __init__(self) -> None:
        self.__I = 0
        self.__V_regs = np.zeros(16, np.uint8)

    def set_I(self, val: int) -> None:
        if val.bit_length() > 16:
            raise TypeError("I register can only be set to 16 bit int")
        self.__I = val

    #TODO: should vf be restricted or sepereated?
    def set_Vx(self, reg_ind: int, val: int) -> None:
        if reg_ind < 0x0 or reg_ind > 0xF:
            raise IndexError(
                f"we dont have register V{reg_ind}, available index 0x0-0xF")
        if val.bit_length() > 8:
            raise TypeError(
                f"V{reg_ind} register can only be set to 8 bit int")
        self.__V_regs[reg_ind] = val

    def get_I(self) -> int:
        return self.__I

    def get_Vx(self, reg_ind: int) -> int:
        if reg_ind < 0x0 or reg_ind > 0xF:
            raise IndexError(
                f"we dont have register V{reg_ind}, available index 0x0-0xF")
        return int(self.__V_regs[reg_ind])
