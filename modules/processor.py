import random
from typing import List
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


def _5xy0(reg:Register,mem:Memory,nd_nimble:int,rd_nimble:int):
    """
    0x5XY0: SE Vx, Vy
    Skip next instruction if Vx = Vy.
    """
    if reg.get_Vx(nd_nimble) == reg.get_Vx(rd_nimble):
        mem.skip()


def _6xkk(reg:Register,nd_nimble:int,nn_nimble:int):
    """
    0x6XKK: LD Vx, byte
    Set Vx = kk.
    """
    reg.set_Vx(nd_nimble,nn_nimble)


def _7xkk(reg:Register,nd_nimble:int,nn_nimble:int):
    """
    0x7XKK: ADD Vx, byte
    Set Vx = Vx + kk.
    """
    vx = reg.get_Vx(nd_nimble)
    res = (vx + nn_nimble) % 0x100
    reg.set_Vx(nd_nimble,res)

def _8xy0(reg:Register,nd_nimble:int,rd_nimble:int):
    """
    0x8XY0: LD Vx, Vy
    Set Vx = Vy.
    """
    reg.set_Vx(nd_nimble,reg.get_Vx(rd_nimble))


def _8xy1(reg:Register,nd_nimble:int,rd_nimble:int):
    """
    0x8XY1: OR Vx, Vy
    Set Vx = Vx OR Vy.
    """
    vx = reg.get_Vx(nd_nimble)
    vy = reg.get_Vx(rd_nimble)
    res = vx | vy
    reg.set_Vx(nd_nimble,res)


def _8xy2(reg:Register,nd_nimble:int,rd_nimble:int):
    """
    0x8XY2: AND Vx, Vy
    Set Vx = Vx AND Vy.
    """
    vx = reg.get_Vx(nd_nimble)
    vy = reg.get_Vx(rd_nimble)
    res = vx & vy
    reg.set_Vx(nd_nimble,res)


def _8xy3(reg:Register,nd_nimble:int,rd_nimble:int):
    """
    0x8XY3: XOR Vx, Vy
    Set Vx = Vx XOR Vy.
    """
    vx = reg.get_Vx(nd_nimble)
    vy = reg.get_Vx(rd_nimble)
    res = vx ^ vy
    reg.set_Vx(nd_nimble,res)


def _8xy4(reg:Register,nd_nimble:int,rd_nimble:int):
    """
    0x8XY4: ADD Vx, Vy
    Set Vx = Vx + Vy, set VF = carry.
    """
    vx = reg.get_Vx(nd_nimble)
    vy = reg.get_Vx(rd_nimble)
    res = (vx + vy)
    reg.set_Vx(0xF, 1) if res > 255 else reg.set_Vx(0xF, 0)
    res %= 0x100
    reg.set_Vx(nd_nimble,res)


def _8xy5(reg:Register,nd_nimble:int,rd_nimble:int):
    """
    0x8XY5: SUB Vx, Vy
    Set Vx = Vx - Vy, set VF = NOT borrow.
    """
    vx = reg.get_Vx(nd_nimble)
    vy = reg.get_Vx(rd_nimble)
    reg.set_Vx(0xF, 1) if vx > vy else reg.set_Vx(0xF, 0)
    res = (vx - vy) % 0x100
    reg.set_Vx(nd_nimble,res)


def _8xy6(reg:Register,nd_nimble:int):
    """
    0x8XY6: SHR Vx {, Vy}
    Set Vx = Vx SHR 1.
    """
    vx = reg.get_Vx(nd_nimble)
    reg.set_Vx(0xF, vx & 0x1)
    vx >>= 1
    reg.set_Vx(nd_nimble,vx)


def _8xy7(reg:Register,nd_nimble:int,rd_nimble:int):
    """
    0x8XY7: SUBN Vx, Vy
    Set Vx = Vy - Vx, set VF = NOT borrow.
    """
    vx = reg.get_Vx(nd_nimble)
    vy = reg.get_Vx(rd_nimble)
    reg.set_Vx(0xF, 1) if vy > vx else reg.set_Vx(0xF, 0)
    res = (vy - vx) % 0x100
    reg.set_Vx(nd_nimble,res)


def _8xye(reg:Register,nd_nimble:int):
    """
    0x8XYE: SHL Vx {, Vy}
    Set Vx = Vx SHL 1.
    """
    vx = reg.get_Vx(nd_nimble)
    reg.set_Vx(0xF, vx >> 7)
    vx <<= 1
    vx &= 0xFF
    reg.set_Vx(nd_nimble,vx)


def _9xy0(reg:Register,mem:Memory,nd_nimble:int,rd_nimble:int):
    """
    0x9XY0: SNE Vx, Vy
    Skip next instruction if Vx != Vy.
    """
    if reg.get_Vx(nd_nimble) != reg.get_Vx(rd_nimble):
        mem.skip()


def annn(reg:Register,nn_nimble:int):
    """
    0xANNN: LD I, addr
    Set I = nnn.
    """
    reg.set_I(nn_nimble)


def bnnn(reg:Register,mem:Memory,nnn_nimble:int):
    """
    0xBNNN: JP V0, addr
    Jump to location nnn + V0.
    """
    mem.set_pc(nnn_nimble + reg.get_Vx(0)) # should this be allowed to overflow


def cxkk(reg:Register,nd_nimble:int,nn_nimble:int):
    """
    0xCXKK: RND Vx, byte
    Set Vx = random byte AND kk.
    """
    reg.set_Vx(nd_nimble,random.randint(0,255) & nn_nimble)


def dxyn(reg:Register,mem:Memory,gui:Gui,nd_nimble:int,rd_nimble:int,th_nimble:int):
    """
    0xDXYN: DRW Vx, Vy, nibble
    Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
    """
    #TODO: fix this, as it wont wrap around the screen
    x = reg.get_Vx(nd_nimble) % Gui.WIDTH
    y = reg.get_Vx(rd_nimble) % Gui.HEIGHT
    n = th_nimble
    mem_loc = reg.get_I()
    reg.set_Vx(0xF, 0)
    for j in range(n):
        nth_byte = mem.get_mem(mem_loc+j)
        for i in range(8):
            if int(nth_byte) & (2**7 >> i):
                is_flipped = gui.set(x+i, y+j)
                if is_flipped:
                    reg.set_Vx(0xF, 1)
    gui.update_display()


def ex9e(reg:Register,mem:Memory,nd_nimble:int,pressed_keys:List[int]):
    """
    0xEX9E: SKP Vx
    Skip next instruction if key with the value of Vx is pressed.
    """
    if reg.get_Vx(nd_nimble) in pressed_keys:
        mem.skip()


def exa1(reg:Register,mem:Memory,nd_nimble:int,pressed_keys:List[int]):
    """
    0xEXA1: SKNP Vx
    Skip next instruction if key with the value of Vx is not pressed.
    """
    if not reg.get_Vx(nd_nimble) in pressed_keys:
        mem.skip()


def fx07(reg:Register,dtimer:DelayTimer,nd_nimble:int):
    """
    0xFX07: LD Vx, DT
    Set Vx = delay timer value.
    """
    reg.set_Vx(nd_nimble,dtimer.get())




