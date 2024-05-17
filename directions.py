from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


    @classmethod
    def set_direction(cls, dirn):
        if abs(dirn[0]) > abs(dirn[1]):
            if dirn[0] > 0:    
                direction = cls.RIGHT
            else:
                direction = cls.LEFT
        else:
            if dirn[1] > 0:    
                direction = cls.DOWN
            else:
                direction = cls.UP

        return direction
