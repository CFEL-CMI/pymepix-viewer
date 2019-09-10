from _ctypes import Structure
from ctypes import c_uint64
from pymepix.processing.FlashID.desy.flash.timeval import timeval


class EventInfo(Structure):
    """This is a collection of all event data

    Members:
        id(int): The actual event identifier
        time(timeval): When did the event appear in unix-time
    """
    _fields_ = [("id", c_uint64), ("time", timeval)]