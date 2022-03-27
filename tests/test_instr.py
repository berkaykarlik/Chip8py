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