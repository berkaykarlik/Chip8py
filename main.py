import argparse
import random
from pathlib import Path
from time import sleep

from py import process

import modules.processor as processor
from modules.gui import Gui
from modules.memory import Memory
from modules.stack import Stack
from modules.register import Register
from modules.timers import DelayTimer, SoundTimer


INSTR_PER_SEC = 1400


def main(rom_path: Path) -> None:
    mem = Memory()
    stack = Stack()
    dtimer = DelayTimer()
    stimer = SoundTimer()
    gui = Gui()
    reg = Register()

    with open(rom_path, 'rb') as rom:
        instr = rom.read()

    for i in range(0, len(instr), 2):
        int_instr = int.from_bytes(instr[i:i + 2], byteorder='big')
        mem.load_instr(int_instr)

    while(True):
        # delay for simulating a more real CHIP-8 experience,  700 instr per second lets say
        sleep(1/INSTR_PER_SEC)

        gui.process_events()
        pressed_keys = gui.get_pool()
        print(f'pressed_keys {pressed_keys}')

        # fetch
        curr_instr = mem.fetch()
        # decode & execute

        # decode once to avoid repetation inside case statements, even if its unnecessary for some instructions
        st_nimble = (curr_instr & 0xF000) >> 12
        nd_nimble = (curr_instr & 0x0F00) >> 8
        rd_nimble = (curr_instr & 0x00F0) >> 4
        th_nimble = curr_instr & 0x000F
        #third and fourth
        nn_nimble = curr_instr & 0x00FF
        #second, third and fourth
        nnn_nimble = curr_instr & 0x0FFF

        match st_nimble:
            case 0x0:
                match nnn_nimble:
                    case 0x0E0:
                        processor._00e0(gui)
                    case 0x0EE:
                        processor._00ee(mem, stack)
                    case 0x000:  # run out of instructions, instr value is empty memory cell
                        print("empty memory")
            case 0x1:
                processor._1nnn(mem, nnn_nimble)
            case 0x2:
                processor._2nnn(stack, mem, nnn_nimble)
            case 0x3:
                processor._3xkk(reg, mem, nd_nimble, nn_nimble)
            case 0x4:
                processor._4xkk(reg, mem, nd_nimble, nn_nimble)
            case 0x5:
                processor._5xy0(reg, mem, nd_nimble, rd_nimble)
            case 0x6:
                processor._6xkk(reg, nn_nimble, nd_nimble)
            case 0x7:  # add value to register
                print("add value to register")
                op_result = (reg.get_Vx(nd_nimble)+nn_nimble) % 256
                reg.set_Vx(nd_nimble, op_result)
            case 0x8:  # Aritmatic and logic ops
                match th_nimble:
                    case 0:  # set
                        print("reg set")
                        reg.set_Vx(nd_nimble, reg.get_Vx(rd_nimble))
                    case 1:  # or
                        print("or")
                        reg.set_Vx(nd_nimble, reg.get_Vx(
                            nd_nimble) | reg.get_Vx(rd_nimble))
                    case 2:  # and
                        print("and")
                        reg.set_Vx(nd_nimble, reg.get_Vx(
                            nd_nimble) & reg.get_Vx(rd_nimble))
                    case 3:  # xor
                        print("xor")
                        reg.set_Vx(nd_nimble, reg.get_Vx(
                            nd_nimble) ^ reg.get_Vx(rd_nimble))
                    case 4:  # add
                        print("add")
                        _sum = reg.get_Vx(nd_nimble) + reg.get_Vx(rd_nimble)
                        reg.set_Vx(nd_nimble, _sum % 256)
                        # set overflow
                        reg.set_Vx(
                            0xF, 1) if _sum > 255 else reg.set_Vx(0xF, 0)
                    case 5:  # substract
                        print("substract")
                        vx = reg.get_Vx(nd_nimble)
                        vy = reg.get_Vx(rd_nimble)
                        _subs = vx - vy
                        reg.set_Vx(0xF, 1) if vx > vy else reg.set_Vx(0xF, 0)
                        reg.set_Vx(nd_nimble, _subs)
                    case 6:  # shift
                        print("right shift")
                        vx = reg.get_Vx(rd_nimble)  # ambigous
                        lsb = vx & 0x01
                        reg.set_Vx(nd_nimble, vx >> 1)
                        reg.set_Vx(0xF, 1) if lsb else reg.set_Vx(0xF, 0)
                    case 7:  # substract
                        print("reverse substract")
                        vx = reg.get_Vx(nd_nimble)
                        vy = reg.get_Vx(rd_nimble)
                        _subs = vy - vx
                        reg.set_Vx(0xF, 1) if vy > vx else reg.set_Vx(0xF, 0)
                        reg.set_Vx(nd_nimble, _subs)
                    case 0xE:  # shift
                        print("left shift")
                        vx = reg.get_Vx(rd_nimble)  # ambigous
                        msb = vx & 0x80
                        vx = (vx << 1) % 256
                        reg.set_Vx(nd_nimble, vx)
                        reg.set_Vx(
                            0xF, 1) if msb else reg.set_Vx(0xF, 0)
            case 0x9:
                print("skip if registers not equal")
                if reg.get_Vx(nd_nimble) != reg.get_Vx(rd_nimble):
                    mem.skip()
            case 0xA:  # set index register
                print("set index register to", hex(nnn_nimble))
                reg.set_I(nnn_nimble)
                print("index reg val ", hex(reg.get_I()))
            case 0xB:
                print("Jump with offset")
                mem.jump(nnn_nimble+reg.get_Vx(0x0))
            case 0xC:
                print("random")
                reg.set_Vx(nd_nimble, random.randint(0, 255) & nn_nimble)
            case 0xD:  # display / draw
                print("display")
                x = reg.get_Vx(nd_nimble) % Gui.WIDTH
                y = reg.get_Vx(rd_nimble) % Gui.HEIGHT
                n = th_nimble
                mem_loc = reg.get_I()
                reg.set_Vx(0xF, 0)
                for j in range(n):
                    nth_byte = mem.get_mem(mem_loc+j)
                    # nth_byte = nth_byte.tobytes()
                    for i in range(8):  # a sprite is 8 pixel wide
                        # if x + i >= Gui.WIDTH or y + j >= Gui.HEIGHT:
                        #     break
                        if int(nth_byte) & (2**7 >> i):
                            is_flipped = gui.set(x+i, y+j)
                            if is_flipped:
                                reg.set_Vx(0xF, 1)
                gui.update_display()
            case 0xE:  # press and skip instr
                match nn_nimble:
                    case 0x9E:
                        print("skip if pressed")
                        if reg.get_Vx(nd_nimble) in pressed_keys:
                            mem.skip()
                    case 0xA1:
                        print("skip if not pressed")
                        if not (reg.get_Vx(nd_nimble) in pressed_keys):
                            mem.skip()
            case 0xF:  # timers
                match nn_nimble:
                    case 0x07:  # read delay timer val
                        print("read delay timer")
                        reg.set_Vx(nd_nimble, dtimer.get())
                    case 0x15:  # set delay timer val
                        print("set delay timer")
                        dtimer.set(reg.get_Vx(nd_nimble))
                    case 0x18:  # set sound timer
                        print("set sound timer")
                        stimer.set(reg.get_Vx(nd_nimble))
                    case 0x1E:  # add to index
                        print("add to index")
                        new_I = reg.get_I()+reg.get_Vx(nd_nimble)
                        # not part of original instruction set but it wont break stuff he said
                        reg.set_Vx(
                            0xF, 1) if new_I > 0x0FFF else reg.set_Vx(0xF, 0)
                        reg.set_I(new_I)
                    case 0x0A:  # wait for key
                        print("waiting for key")
                        if not pressed_keys:
                            mem.set_pc(mem.get_pc()-0x2)
                        else:
                            reg.set_Vx(nd_nimble, pressed_keys[0])
                    case 0x29:  # get font
                        print("get font")
                        reg.set_I(0x50+(nd_nimble*5))
                    case 0x33:  # binar coded decimal conversion
                        print("binary coded decimal conversion")
                        val = reg.get_Vx(nd_nimble)
                        dgt1 = val % 10
                        dgt2 = ((val % 100) - dgt1) // 10
                        dgt3 = (val - (val % 100)) // 100
                        mem.set_mem(reg.get_I(), dgt3)
                        mem.set_mem(reg.get_I()+0x1, dgt2)
                        mem.set_mem(reg.get_I()+0x2, dgt1)
                    case 0x55:  # store mem
                        print("store mem")
                        for i in range(nd_nimble+1):
                            mem.set_mem(reg.get_I()+i, reg.get_Vx(i))
                    case 0x65:  # load mem
                        print("load mem")
                        for i in range(nd_nimble+1):
                            reg.set_Vx(i, mem.get_mem(reg.get_I()+i))
            case _:
                print(f"not implemented: {curr_instr} type {st_nimble}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='chip-8 code interpreter')
    parser.add_argument('rom_path', type=Path,
                        nargs=1, help='.ch8 file path, i.e rom to interpret')
    args = parser.parse_args()
    main(args.rom_path[0])
