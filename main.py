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
        instr_type = int.from_bytes(curr_instr, 'big') & 0xF000

        match instr_type:
            case 0x0000:
                print("clear screen")
            case 0x1000:
                print("jump")
            case 0x6000:
                print("set register")
            case 0x7000:
                print("add value to register")
            case 0xA000:
                print("set index register")
            case 0xD000:
                print("display")
            case _:
                print(
                    f"not implemented: {curr_instr.hex()} type {hex(instr_type)}")


if __name__ == '__main__':
    main()
