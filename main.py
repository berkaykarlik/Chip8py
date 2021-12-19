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
        if curr_instr == b'\x00\x00':
            break

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
                print("clear screen")
                if curr_instr == b"\x00\x0e":
                    gui.clear_screen()
            case 0x1:
                print("jump")
                mem.jump(nnn_nimble)
            case 0x2:

                pass
            case 0x3:
                pass
            case 0x4:
                pass
            case 0x5:
                pass
            case 0x6:
                print("set register")
            case 0x7:
                print("add value to register")
            case 0x8:
                pass
            case 0x9:
                pass
            case 0xA:
                print("set index register")
            case 0xB:
                pass
            case 0xC:
                pass
            case 0xD:
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
