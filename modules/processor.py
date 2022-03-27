from modules.gui import Gui
from modules.memory import Memory
from modules.stack import Stack
from modules.register import Register
from modules.timers import DelayTimer, SoundTimer

def _0nnn():
    """
    0x0NNN: SYS addr
    Jump to a machine code routine at nnn.
    """
    #raise NotImplementedError so that we will now if a program is trying to jump to a machine code routine
    raise NotImplementedError("Program tried to jump to a machine code routine")

def _00e0(gui:Gui):
    """
    0x00E0: CLS
    Clear the display.
    """
    gui.clear_screen()


def _00ee(mem:Memory,stack:Stack):
    """
    0x00EE: RET
    Return from a subroutine.
    """
    #pop the top value from the stack and jump to it
    return mem.jump(stack.pop())


def _1nnn(mem:Memory,nnn_nimble:int):
    """
    0x1NNN: JP addr
    Jump to location nnn.
    """
    return mem.jump(nnn_nimble)


def _2nnn(stack:Stack,mem:Memory,nnn_nimble:int):
    """
    0x2NNN: CALL addr
    Call subroutine at nnn.
    """
    stack.push(mem.get_pc())
    mem.jump(nnn_nimble)


def _3xkk(reg:Register,mem:Memory,nd_nimble:int,nn_nimble:int):
    """
    0x3XKK: SE Vx, byte
    Skip next instruction if Vx = kk.
    """
    if reg.get_Vx(nd_nimble) == nn_nimble:
        mem.skip()


def _4xkk(reg:Register,mem:Memory,nd_nimble:int,nn_nimble:int):
    """
    0x4XKK: SNE Vx, byte
    Skip next instruction if Vx != kk.
    """
    if reg.get_Vx(nd_nimble) != nn_nimble:
        mem.skip()
