from enum import Enum

class Direction(Enum):
    '''
    Enum representing directions in a 2D coordinate system.

    Attributes:
        UP: Represents the upward direction as a tuple (0, -1).
        DOWN: Represents the downward direction as a tuple (0, 1).
        LEFT: Represents the leftward direction as a tuple (-1, 0).
        RIGHT: Represents the rightward direction as a tuple (1, 0).
    '''
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def set_direction(cls, dirn):
        '''
        Determines and returns the Direction enum value based on a given direction vector.

        Args:
            dirn (tuple): A tuple representing the direction vector (dx, dy).

        Returns:
            Direction: The Direction enum value corresponding to the given direction vector.
        '''
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
