from enum import Enum

class Position(Enum):
    """
    Used to determin ellipse position inside tower menu.
    """
    
    TOP_RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM = 3
    BOTTOM_LEFT = 4
    TOP_LEFT = 5
    TOP = 0