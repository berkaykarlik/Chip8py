from gui import Gui
from memory import Memory
from stack import Stack
from timers import DelayTimer, SoundTimer


def main():
    mem = Memory()
    stack = Stack()
    dtimer = DelayTimer()
    stimer = SoundTimer()
    gui = Gui()

    with open("roms\IBM Logo.ch8", 'rb') as rom:
        instr = rom.read()

    for i in range(len(instr)//2):
        mem.load_instr(instr[i:i+2])

    while(True):
        # fetch
        curr_instr = mem.fetch()
        # decode & execute

        # decode once to avoid repetation inside case statements, even if its unnecessary for some instructions
        instr_int = int.from_bytes(curr_instr, 'big')
        st_nimble = (instr_int & 0xF000) >> 12
        nd_nimble = (instr_int & 0x0F00) >> 8
        rd_nimble = (instr_int & 0x00F0) >> 4
        th_nimble = instr_int & 0x000F
        #thrid and fourth
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
                        print("finish")
                        break
            case 0x1:  # jump
                print("jump")
                mem.jump(nnn_nimble)
            case 0x2:  # call subroutine
                print("call subroutine")
                stack.push(mem.get_pc)
                mem.jump(nnn_nimble)
            case 0x3:
                pass
            case 0x4:
                pass
            case 0x5:
                pass
            case 0x6:  # set register
                print("set register")
            case 0x7:  # add value to register
                print("add value to register")
            case 0x8:
                pass
            case 0x9:
                pass
            case 0xA:  # set index register
                print("set index register")
            case 0xB:
                pass
            case 0xC:
                pass
            case 0xD:  # display / draw
                print("display")
            case 0xE:
                pass
            case 0xF:
                pass
            case _:
                print(
                    f"not implemented: {curr_instr.hex()} type {hex(st_nimble)}")


if __name__ == '__main__':
    main()
