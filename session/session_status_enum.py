from enum import Enum


class SessionStatusEnum(Enum):
    """
    The SessionStatusEnum designates how a Multivac session concluded.
    """

    # Success indicates the Multivac session was able to run successfully, i.e. agent is able to take the desired
    # number of actions along with the output video being generated.
    SUCCESS = 1

    # Failed indicates the Multivac session raised an Exception.
    FAILED = 3
