import pytest
from memory import Memory



def check_restricted_mem_access(mem: Memory):
    """check if the restricted memory is not accessed"""
    return mem._Memory__memory[0x00:0x50].any() == 0 and mem._Memory__memory[0xA1:Memory.LOWER_MEM_LIM].any() == 0


def test_get_set():
    """set all usable memory and check if they are set correctly,
        also check if the restricted memory is not set"""
    tmp_mem = Memory()

    for i in range (Memory.LOWER_MEM_LIM, Memory.UPPER_MEM_LIM + 1):
        value_to_set = i% 2**8 # 8 bit
        tmp_mem.set_mem(i, value_to_set)
        retrived_val =  tmp_mem.get_mem(i)
        assert retrived_val == value_to_set
        #check if retrived_val is of type int
        assert isinstance(retrived_val, int)

    for i in range (Memory.LOWER_MEM_LIM, Memory.UPPER_MEM_LIM + 1):
        value_to_set = i% 2**8 # 8 bit
        retrived_val =  tmp_mem.get_mem(i)
        assert retrived_val == value_to_set

    assert check_restricted_mem_access(tmp_mem)

    #test setting memory above limit
    with pytest.raises(IndexError) as e_info:
        tmp_mem.set_mem(Memory.UPPER_MEM_LIM+1, 0xFF)

    #test setting memory below limit
    with pytest.raises(IndexError) as e_info:
        tmp_mem.set_mem(Memory.LOWER_MEM_LIM-1, 0xFF)

    #test accessing between 0x50:0xA1
    tmp_mem.get_mem(0x50)


def test_load_and_fetch():
    """load instructions to memory and check if they are loaded correctly"""
    for  i in range(Memory.LOWER_MEM_LIM,Memory.UPPER_MEM_LIM + 1):
        tmp_mem = Memory()
        instr_2byte = i% 2**16 # 16 bit
        tmp_mem.load_instr(instr_2byte)
        fetched_val = tmp_mem.fetch()
        assert fetched_val == instr_2byte
        #check if fetched_val is of type int
        assert isinstance(fetched_val, int)


def test_pc():
    """check if the pc is set correctly"""
    tmp_mem = Memory()
    tmp_mem.set_pc(0x578)
    assert tmp_mem.get_pc() == 0x578

    #test setting pc above limit
    with pytest.raises(IndexError) as e_info:
        tmp_mem.set_pc(Memory.UPPER_MEM_LIM+1)

    #test setting pc below limit
    with pytest.raises(IndexError) as e_info:
        tmp_mem.set_pc(Memory.LOWER_MEM_LIM-1)


def test_jump():
    """check if the pc is set correctly"""
    tmp_mem = Memory()
    tmp_mem.set_pc(0x578)
    tmp_mem.jump(0x600)
    assert tmp_mem.get_pc() == 0x600

    #test jumping above limit
    with pytest.raises(IndexError) as e_info:
        tmp_mem.jump(Memory.UPPER_MEM_LIM+1)

    #test jumping below limit
    with pytest.raises(IndexError) as e_info:
        tmp_mem.jump(Memory.LOWER_MEM_LIM-1)
