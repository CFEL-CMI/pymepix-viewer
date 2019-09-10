from _ctypes import Structure
from ctypes import c_long


class timeval(Structure):
    """ This struct contains the unix timestamp of the event """
    _fields_ = [("tv_sec", c_long), ("tv_usec", c_long)]