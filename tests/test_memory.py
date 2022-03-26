from memory import Memory


def check_restricted_mem_access(mem: Memory):
    """check if the restricted memory is not accessed"""
    return mem._Memory__memory[0x00:0x50].any() == 0 and mem._Memory__memory[0xA1:0x200].any() == 0


def test_get_set():
    """set all usable memory and check if they are set correctly,
        also check if the restricted memory is not set"""
    tmp_mem = Memory()

    for i in range (Memory.LOWER_MEM_LIM, Memory.UPPER_MEM_LIM + 1):
        value_to_set = i% 2**8 # 8 bit
        tmp_mem.set_mem(i, value_to_set)
        retrived_val =  tmp_mem.get_mem(i)
        assert retrived_val == value_to_set

    for i in range (Memory.LOWER_MEM_LIM, Memory.UPPER_MEM_LIM + 1):
        value_to_set = i% 2**8 # 8 bit
        retrived_val =  tmp_mem.get_mem(i)
        assert retrived_val == value_to_set

    assert check_restricted_mem_access(tmp_mem)

