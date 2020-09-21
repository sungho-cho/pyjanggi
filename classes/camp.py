from enum import IntEnum

class Camp(IntEnum):
    CHO = 0
    HAN = 1

    def opponent(self):
        return Camp(1-self)