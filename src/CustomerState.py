from enums import Enum


class CustomerState(Enum):
    ENTERED = 1
    SHOPPING = 2
    CHOOSING_QUEUE = 3
    QUEUED = 4
    PAYING = 5
    EXITING = 6
