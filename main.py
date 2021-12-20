from time import sleep
import random
from gui import Gui
from memory import Memory
from stack import Stack
from register import Register
from timers import DelayTimer, SoundTimer

INSTR_PER_SEC = 700


def main() -> None:
    mem = Memory()
    stack = Stack()
    dtimer = DelayTimer()
    stimer = SoundTimer()
    gui = Gui()
    reg = Register()

    with open("roms\ibm_logo.ch8", 'rb') as rom:
        instr = rom.read()

    for i in range(0, len(instr), 2):
        mem.load_instr(instr[i:i+2])

    while(True):
        # delay for simulating a more real CHIP-8 experience,  700 instr per second lets say
        sleep(1/INSTR_PER_SEC)

        pressed_keys = gui.process_events()

        # fetch
        curr_instr = mem.fetch()
        # decode & execute
        print(f"curr_instr {curr_instr.hex()}")

        # decode once to avoid repetation inside case statements, even if its unnecessary for some instructions
        instr_int = int.from_bytes(curr_instr, 'big')
        st_nimble = (instr_int & 0xF000) >> 12
        nd_nimble = (instr_int & 0x0F00) >> 8
        rd_nimble = (instr_int & 0x00F0) >> 4
        th_nimble = instr_int & 0x000F
        #third and fourth
        nn_nimble = instr_int & 0x00FF
        #second, third and fourth
        nnn_nimble = instr_int & 0x0FFF

        match st_nimble:
            case 0x0:
                match nnn_nimble:
                    case 0x0E0:  # clear screen
                        print("clear screen")
                        gui.clear_screen()
                    case 0x0EE:  # return from subroutine
                        print("return from subroutine")
                        mem.jump(stack.pop())
                    case 0x000:  # run out of instructions, instr value is empty memory cell
                        print("empty memory")
            case 0x1:  # jump
                print("jump")
                mem.jump(nnn_nimble)
            case 0x2:  # call subroutine
                print("call subroutine")
                stack.push(mem.get_pc())
                mem.jump(nnn_nimble)
            case 0x3:  # skip one instruction if equal
                print("skip if equal")
                if reg.get_Vx(nd_nimble) == nnn_nimble:
                    mem.skip()
            case 0x4:  # skip one instruction if not equal
                print("skip if not equal")
                if reg.get_Vx(nd_nimble) != nnn_nimble:
                    mem.skip()
            case 0x5:  # skip if second and third nimble indexed registers are equal
                print("skip if registers equal")
                if reg.get_Vx(nd_nimble) == reg.get_Vx(th_nimble):
                    mem.skip()
            case 0x6:  # set register
                print(f"set register v{nd_nimble} to {hex(nn_nimble)} ")
                reg.set_Vx(nd_nimble, nn_nimble)
                print("register set to ", hex(reg.get_Vx(nd_nimble)))
            case 0x7:  # add value to register
                print("add value to register")
                op_result = (reg.get_Vx(nd_nimble)+nn_nimble) & 0xFF
                reg.set_Vx(nd_nimble, op_result)
            case 0x8:  # Aritmatic and logic ops
                match th_nimble:
                    case 0:  # set
                        print("reg set")
                        reg.set_Vx(nd_nimble, reg.get_Vx(rd_nimble))
                    case 1:  # or
                        print("or")
                        reg.set_Vx(nd_nimble, reg.get_Vx(
                            nd_nimble) & reg.get_Vx(rd_nimble))
                    case 2:  # and
                        print("and")
                        reg.set_Vx(nd_nimble, reg.get_Vx(
                            nd_nimble) | reg.get_Vx(rd_nimble))
                    case 3:  # xor
                        print("xor")
                        reg.set_Vx(nd_nimble, reg.get_Vx(
                            nd_nimble) ^ reg.get_Vx(rd_nimble))
                    case 4:  # add
                        print("add")
                        _sum = reg.get_Vx(nd_nimble) + reg.get_Vx(rd_nimble)
                        reg.set_Vx(nd_nimble, _sum)
                        # set overflow
                        reg.set_Vx(
                            0xF, 1) if _sum > 255 else reg.set_Vx(0xF, 0)
                    case 5:  # substract
                        print("substract")
                        _subs = reg.get_Vx(nd_nimble) - reg.get_Vx(rd_nimble)
                        reg.set_Vx(
                            0xF, 1) if _subs > 0 else reg.set_Vx(0xF, 0)
                        reg.set_Vx(nd_nimble, _subs)
                    case 6:  # shift
                        print("right shift")
                        vx = reg.get_Vx(rd_nimble)
                        shifted_bit = vx & 0x01
                        reg.set_Vx(vx >> 2)
                        reg.set_Vx(
                            0xF, 1) if shifted_bit else reg.set_Vx(0xF, 0)
                    case 7:  # substract
                        print("reverse substract")
                        _subs = reg.get_Vx(rd_nimble) - reg.get_Vx(nd_nimble)
                        reg.set_Vx(
                            0xF, 1) if _subs > 0 else reg.set_Vx(0xF, 0)
                        reg.set_Vx(nd_nimble, _subs)
                    case 0xE:  # shift
                        print("left shift")
                        vx = reg.get_Vx(rd_nimble)
                        shifted_bit = vx & 0x80
                        reg.set_Vx(vx << 2)
                        reg.set_Vx(
                            0xF, 1) if shifted_bit else reg.set_Vx(0xF, 0)
            case 0x9:
                print("skip if registers not equal")
                if reg.get_Vx(nd_nimble) != reg.get_Vx(th_nimble):
                    mem.skip()
            case 0xA:  # set index register
                print("set index register to", hex(nnn_nimble))
                reg.set_I(nnn_nimble)
                print("index reg val ", hex(reg.get_I()))
            case 0xB:
                print("Jump with offset")
                mem.jump(nnn_nimble+reg.get_Vx(0x0))
            case 0xC:
                reg.set_Vx(nd_nimble, random.randint() & nn_nimble)
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
                        if reg.get_Vx(nd_nimble) in pressed_keys:
                            mem.skip()
                    case 0xA1:
                        if not (reg.get_Vx(nd_nimble) in pressed_keys):
                            mem.skip()
            case 0xF:  # timers
                match nn_nimble:
                    case 0x07:  # read delay timer val
                        reg.set_Vx(nd_nimble, dtimer.get())
                    case 0x15:  # set delay timer val
                        dtimer.set(reg.get_Vx(nd_nimble))
                    case 0x18:  # set sound timer
                        stimer.set(reg.get_Vx(nd_nimble))
                    case 0x1E:
                        new_I = reg.get_I()+reg.get_Vx(nd_nimble)
                        # not part of original instruction set but it wont break stuff he said
                        reg.set_Vx(
                            0xF, 1) if new_I > 0x0FFF else reg.set_Vx(0xF, 0)
                        reg.set_I()
                    case 0x0A:
                        if not pressed_keys:
                            mem.set_pc(mem.get_pc()-0x2)
                        else:
                            reg.set_Vx(nd_nimble, pressed_keys[0])

            case _:
                print(
                    f"not implemented: {curr_instr.hex()} type {hex(st_nimble)}")


if __name__ == '__main__':
    main()
