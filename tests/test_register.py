import pytest
from modules.register import Register


def test_I():
    regs = Register()
    regs.set_I(0xFF)
    assert regs.get_I() == 0xFF

    #test setting more than 2 bytes
    with pytest.raises(ValueError) as e_info:
        regs.set_I(0xFFFFF)


def test_Vx():
    regs = Register()
    regs.set_Vx(0x0, 0xFF)
    assert regs.get_Vx(0x0) == 0xFF

    #test setting reg_ind above F
    with pytest.raises(IndexError) as e_info:
        regs.set_Vx(0x10, 0xFF)

    #test setting reg_ind below 0
    with pytest.raises(IndexError) as e_info:
        regs.set_Vx(-1, 0xFF)

    #test setting more than 1 byte
    with pytest.raises(ValueError) as e_info:
        regs.set_Vx(0x0, 0xFFF)