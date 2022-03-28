import time
import pytest
from modules.gui import Gui
import modules.processor as processor

def test__0nnn():
    """
    0x0NNN: SYS addr
    Jump to a machine code routine at nnn.
    """
    #raises NotImplementedError so that we will now if a program is trying to jump to a machine code routine
    with pytest.raises(NotImplementedError):
        processor._0nnn()

def test_00e0():
    """
    0x00E0: CLS
    Clear the display.
    """
    gui = Gui()
    processor._00e0(gui)

    assert gui._Gui__frame.any() == 0

def test_00ee():
    """
    0x00EE: RET
    Return from a subroutine.
    """
    mem = processor.Memory()
    stack = processor.Stack()
    stack.push(0xFFE)
    processor._00ee(mem,stack)
    assert mem.get_pc() == 0xFFE


def test_1nnn():
    """
    0x1NNN: JP addr
    Jump to location nnn.
    """
    mem = processor.Memory()
    processor._1nnn(mem,0xFFE)
    assert mem.get_pc() == 0xFFE


def test_2nnn():
    """
    0x2NNN: CALL addr
    Call subroutine at nnn.
    """
    stack = processor.Stack()
    mem = processor.Memory()
    processor._2nnn(stack,mem,0xFF1)
    assert stack.pop() == 0x200
    assert mem.get_pc() == 0xFF1


def test_3xkk():
    """
    0x3XKK: SE Vx, byte
    Skip next instruction if Vx = kk.
    """
    mem = processor.Memory()
    reg = processor.Register()
    reg.set_Vx(0x0,0xFF)
    processor._3xkk(reg,mem,0x0,0xFF)
    assert mem.get_pc() == 0x202
    processor._3xkk(reg,mem,0x0,0x1)
    assert mem.get_pc() == 0x202


def test_4xkk():
    """
    0x4XKK: SNE Vx, byte
    Skip next instruction if Vx != kk.
    """
    mem = processor.Memory()
    reg = processor.Register()
    reg.set_Vx(0x0,0xFF)
    processor._4xkk(reg,mem,0x0,0x1)
    assert mem.get_pc() == 0x202
    processor._4xkk(reg,mem,0x0,0xFF)
    assert mem.get_pc() == 0x202


def test_5xy0():
    """
    0x5XY0: SE Vx, Vy
    Skip next instruction if Vx = Vy.
    """
    mem = processor.Memory()
    reg = processor.Register()
    reg.set_Vx(0x0,0xFF)
    reg.set_Vx(0x1,0xFF)
    processor._5xy0(reg,mem,0x0,0x1)
    assert mem.get_pc() == 0x202
    processor._5xy0(reg,mem,0x0,0x2)
    assert mem.get_pc() == 0x202


def test_6xkk():
    """
    0x6XKK: LD Vx, byte
    Set Vx = kk.
    """
    reg = processor.Register()
    processor._6xkk(reg,0x0,0xFF)
    assert reg.get_Vx(0x0) == 0xFF


def test_7xkk():
    """
    0x7XKK: ADD Vx, byte
    Set Vx = Vx + kk.
    """
    reg = processor.Register()
    reg.set_Vx(0x0,0xFF)
    processor._7xkk(reg,0x0,0xFF)
    assert reg.get_Vx(0x0) == (0xFF + 0xFF) % 0x100


def test_8xy0():
    """
    0x8XY0: LD Vx, Vy
    Set Vx = Vy.
    """
    reg = processor.Register()
    reg.set_Vx(0x0,0x09)
    reg.set_Vx(0x1,0xFF)
    processor._8xy0(reg,0x0,0x1)
    assert reg.get_Vx(0x0) == reg.get_Vx(0x1)


def test_8xy1():
    """
    0x8XY1: OR Vx, Vy
    Set Vx = Vx OR Vy.
    """
    reg = processor.Register()
    reg.set_Vx(0x0,0x00)
    reg.set_Vx(0x1,0xFF)
    processor._8xy1(reg,0x0,0x1)
    assert reg.get_Vx(0x0) == 0xFF


def test_8xy2():
    """
    0x8XY2: AND Vx, Vy
    Set Vx = Vx AND Vy.
    """
    reg = processor.Register()
    reg.set_Vx(0x0,0x00)
    reg.set_Vx(0x1,0xFF)
    processor._8xy2(reg,0x0,0x1)
    assert reg.get_Vx(0x0) == 0x00


def test_8xy3():
    """
    0x8XY3: XOR Vx, Vy
    Set Vx = Vx XOR Vy.
    """
    reg = processor.Register()
    reg.set_Vx(0x0,0xF0)
    reg.set_Vx(0x1,0xFF)
    processor._8xy3(reg,0x0,0x1)
    assert reg.get_Vx(0x0) == 0x0F


def test_8xy4():
    """
    0x8XY4: ADD Vx, Vy
    Set Vx = Vx + Vy, set VF = carry.
    """
    reg = processor.Register()
    reg.set_Vx(0x3,0xFF)
    reg.set_Vx(0x4,0xFF)
    processor._8xy4(reg,0x3,0x4)
    assert reg.get_Vx(0x3) == 0xFE
    assert reg.get_Vx(0xF) == 1


def test_8xy5():
    """
    0x8XY5: SUB Vx, Vy
    Set Vx = Vx - Vy, set VF = NOT borrow.
    """
    reg = processor.Register()
    reg.set_Vx(0x3,0xFF)
    reg.set_Vx(0x4,0x01)
    processor._8xy5(reg,0x3,0x4)
    assert reg.get_Vx(0x3) == 0xFE
    assert reg.get_Vx(0xF) == 1

    reg.set_Vx(0x3,0x01)
    reg.set_Vx(0x4,0xFF)
    processor._8xy5(reg,0x3,0x4)
    assert reg.get_Vx(0x3) == (0x01 - 0xFF) % 0x100
    assert reg.get_Vx(0xF) == 0


def test_8xy6():
    """
    0x8XY6: SHR Vx {, Vy}
    Set Vx = Vx SHR 1.
    """
    reg = processor.Register()
    reg.set_Vx(0x0,0xFF)
    processor._8xy6(reg,0x0)
    assert reg.get_Vx(0x0) == (0xFF >> 1)
    assert reg.get_Vx(0xF) == 1

    reg.set_Vx(0x0,0xF0)
    processor._8xy6(reg,0x0)
    assert reg.get_Vx(0x0) == (0xF0 >> 1)
    assert reg.get_Vx(0xF) == 0


def test_8xy7():
    """
    0x8XY7: SUBN Vx, Vy
    Set Vx = Vy - Vx, set VF = NOT borrow.
    """
    reg = processor.Register()
    reg.set_Vx(0x3,0xFF)
    reg.set_Vx(0x4,0x01)
    processor._8xy7(reg,0x3,0x4)
    assert reg.get_Vx(0x3) == (0x01 - 0xFF) % 0x100
    assert reg.get_Vx(0xF) == 0

    reg.set_Vx(0x3,0x01)
    reg.set_Vx(0x4,0xFF)
    processor._8xy7(reg,0x3,0x4)
    assert reg.get_Vx(0x3) == 0xFE
    assert reg.get_Vx(0xF) == 1


def test_8xye():
    """
    0x8XYE: SHL Vx {, Vy}
    Set Vx = Vx SHL 1.
    """
    reg = processor.Register()
    reg.set_Vx(0x0,0xFF)
    processor._8xye(reg,0x0)
    assert reg.get_Vx(0x0) == (0xFF << 1) % 0x100
    assert reg.get_Vx(0xF) == 1

    reg.set_Vx(0x0,0x01)
    processor._8xye(reg,0x0)
    assert reg.get_Vx(0x0) == (0x01 << 1)
    assert reg.get_Vx(0xF) == 0


def test_9xy0():
    """
    0x9XY0: SNE Vx, Vy
    Skip next instruction if Vx != Vy.
    """
    reg = processor.Register()
    mem = processor.Memory()
    reg.set_Vx(0x0,0xFF)
    reg.set_Vx(0x1,0xFF)
    processor._9xy0(reg,mem,0x0,0x1)
    assert mem.get_pc() == 0x200

    reg.set_Vx(0x0,0x00)
    processor._9xy0(reg,mem,0x0,0x1)
    assert mem.get_pc() == 0x202


def test_annn():
    """
    0xANNN: LD I, addr
    Set I = nnn.
    """
    reg = processor.Register()
    mem = processor.Memory()
    processor.annn(reg,0xABD)
    assert reg.get_I() == 0xABD


def test_bnnn():
    """
    0xBNNN: JP V0, addr
    Jump to location nnn + V0.
    """
    reg = processor.Register()
    mem = processor.Memory()
    reg.set_Vx(0x0,0xAB)
    processor.bnnn(reg,mem,0xABC)
    assert mem.get_pc() == 0xABC + 0xAB


def test_cxkk():
    """
    0xCXKK: RND Vx, byte
    Set Vx = random byte AND kk.
    """
    reg = processor.Register()
    processor.cxkk(reg,0x0,0x00) # all we can test if and is working
    assert reg.get_Vx(0x0) == 0


def test_dxyn():
    """
    0xDXYN: DRW Vx, Vy, nibble
    Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
    """
    #TODO: implement this test
    pass


def test_ex9e():
    """
    0xEX9E: SKP Vx
    Skip next instruction if key with the value of Vx is pressed.
    """
    reg = processor.Register()
    mem = processor.Memory()
    reg.set_Vx(0x0,0x07)
    processor.ex9e(reg,mem,0x0,[0x7,0x0])
    assert mem.get_pc() == 0x202

    processor.ex9e(reg,mem,0x0,[0x8,0x0])
    assert mem.get_pc() == 0x202


def test_exa1():
    """
    0xEXA1: SKNP Vx
    Skip next instruction if key with the value of Vx is not pressed.
    """
    reg = processor.Register()
    mem = processor.Memory()
    reg.set_Vx(0x0,0x07)
    processor.exa1(reg,mem,0x0,[0x1,0x0])
    assert mem.get_pc() == 0x202

    processor.exa1(reg,mem,0x0,[0x7,0x0])
    assert mem.get_pc() == 0x202


def test_fx07():
    """
    0xFX07: LD Vx, DT
    Set Vx = delay timer value.
    """
    reg = processor.Register()
    dtimer = processor.DelayTimer()
    dtimer.set(145)
    time.sleep(0.5)
    processor.fx07(reg,dtimer,0x7)
    assert reg.get_Vx(0x7) <= 145


def test_fx0a():
    """
    0xFX0A: LD Vx, K
    Wait for a key press, store the value of the key in Vx.
    """
    reg = processor.Register()
    mem = processor.Memory()

    mem.set_pc(0x400)
    processor.fx0a(reg,mem,[],0x5)
    assert mem.get_pc() == 0x3FE
    processor.fx0a(reg,mem,[],0x5)
    assert mem.get_pc() == 0x3FC

    processor.fx0a(reg,mem,[0x5],0x5)
    assert reg.get_Vx(0x5) == 0x5
    assert mem.get_pc() == 0x3FC


def test_fx15():
    """
    0xFX15: LD DT, Vx
    Set delay timer = Vx.
    """
    reg = processor.Register()
    dtimer = processor.DelayTimer()
    reg.set_Vx(0x7,0x15)
    processor.fx15(reg,dtimer,0x7)
    assert dtimer._DelayTimer__value == reg.get_Vx(0x7)