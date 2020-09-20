from enum import Enum

class Camp(Enum):
    CHO = 0
    HAN = 1

    def __init__(self, campNum):
        self.campNum = campNum

    @property
    def opponent(self):
        return Camp(1-self.campNum)