from enum import Enum

class Target(Enum):
    """
    Used to determine which enemy tower should target.
    """

    FIRST = "First"
    LAST = "Last"
    MOST_HEALTH = "Most health"
    LEAST_HEALTH = "Least health"
    ALL = "All"
    NOT_SET = "Not set"
