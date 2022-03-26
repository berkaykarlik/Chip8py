"""a class for representing CHIP-8 stack"""


class Stack():
    def __init__(self) -> None:
        # plot twist stack was a list all along
        self.__stack = []
        # it seeems back then tere was a limit, so lets pretend we dont have 8gb ram
        self.__stack_limit = 16 #or 12?

    def push(self, item: int):
        if len(self.__stack) > self.__stack_limit:
            return
        if item.bit_length() > 16:
            raise TypeError("stack entries must be 16 bit int")
        self.__stack.append(item)
        return True

    def pop(self):
        if self.__stack:
            return self.__stack.pop()
        return None

    def __repr__(self) -> str:
        return 'bottom -> ' + ' '.join(list(map(str, self.__stack))) + ' <- top'
