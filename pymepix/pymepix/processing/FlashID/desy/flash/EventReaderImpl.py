""" desy.flash.EventReaderImpl

    :copyright: 2019 DESY
    :license: GPL v3, see http://www.gnu.org/licenses/
"""

import select
import socket
import time

from threading import Thread

from pymepix.processing.FlashID.desy.flash.EventInfo import EventInfo
from pymepix.processing.FlashID.desy.flash.timeval import timeval


class AbstractReaderImpl:
    """This implements the basic functionality of receiving"""

    def __init__(self):
        self.notify = False
        self._listeners = []
        self._sock = None
        self._thread = None

    def __del__(self):
        self._stop_receiving()
        print("All dead")

    def register_listener(self, listener):
        self._listeners.append(listener)

    def unregister_listener(self, listener):
        self._listeners.remove(listener)

    def connect(self, host, port):
        """ Connects the socket to its remote """
        self._stop_receiving()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # We would like to bind the local port also the destination
        # port. But it is not needed, so we disable it for now.
#        if hasattr(socket, 'SO_REUSEPORT'):
#            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#        if hasattr(socket, 'SO_REUSEADDR'):
#            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#        self._sock.bind(("", 58050))

        self._sock.connect((host, port))
        self._sock.setblocking(False)
        self._start_receiving()
        return True

    def _receiving_proc(self):
        """The function doing all the socket processing"""
        timeout = 100
        while self._sock is not None:
            try:
                (r, w, e) = select.select([self._sock], [], [], timeout)
                if self._sock in r:
                    data = self._sock.recv(32)
                    if not data:
                        break
                    msg = data.decode('ascii').strip(" \r\n")
                    event = self._analyze(msg)
                    event = self._process(event)
                    if event is not None:
                        self._notify_listeners(event)
                    else:
                        self._notify_listeners_disconnect()
            except (socket.timeout, socket.error) as e:
                print(f"Error in receive: {e}")
                break  # leave the look
        self._stop_receiving()
        print("Receiving thread is dead!")

    # TODO: needs implementation
    def _analyze(self, msg):
        t = None
        # this is error prone like hell, but I have no better idea
        try:
            t = time.mktime(time.strptime(msg[0:12], "%y%m%d %H%M%S"))
        except:
            print(f"message \"{msg}\" is not as expected!")
            return None
        usec = int(msg[14:17])
        id = int(msg[18:26], 16)

        return EventInfo(id=id, time=timeval(tv_sec=int(t), tv_usec=usec))

    def _process(self, event):
        """ allow post-processing of events"""
        return event

    # TODO: figure out how to start the thread
    def _start_receiving(self):
        """Start the receiving thread/co-routine"""
        self._thread = Thread(target=self._receiving_proc, name='ReceiverThread')
        return self._thread.start()

    def _stop_receiving(self):
        """Stop the receiving thread and close the socket"""
        if self._sock is not None:
            print("Stopping receive...")
            self._sock.close()
            self._sock = None
        if self._thread is not None:
            print(" > waiting for thread to die...")
            self._thread.join()
            print(" > thread is dead")
            self._thread = None


    # TODO: this is sequential, problematic if one listener blocks or needs longer
    #       might need to be changed to something async
    def _notify_listeners(self, event):
        if self.notify:
            for i in self._listeners:
                i.on_event(event)

    def _notify_listeners_disconnect(self, reason):
        for i in self._listeners:
            i.on_disconnect(reason)


# class Event(Structure):
#     """Used in JitterImpl"""
#     _fields_ = [("id", c_uint64), ("offset", c_uint64), ("time", timeval)]
#
#
# class ID(Structure):
#     """Used in JitterImpl"""
#     _fields_ = [("id_iq", c_uint32), ("id_sub", c_uint32), ("jitter", c_uint32), ("jitter0", c_uint32)]
#
#
# class JitterImpl(AbstractReaderImpl):
#     """This adds support for eliminating event jitter caused by the network"""
#     LIST_SIZE = 40
#
#     def __init__(self):
#         self._events = []
#         self._event_index = -1
#
#     def _process(self, event):
#         # make sure the data is analyzed before doing further processing
#         super(JitterImpl, self)._process(event)
#         # queue up the filter buffer
#         tv = self._event.time
#         offset = tv.tv_usec + 1000000 * tv.tv_sec - 100000 * self._event.id
#         # fill all buffers with the current event
#         if self._event_index == -1:
#             e = Event(id=self._event.id, offset=offset, timel=self._event.time)
#             for i in range(0, self.LIST_SIZE):
#                 self._events.append(e)
#
#         # update the current buffer entry
#         self._events[self._event_index].time.tv_sec = tv.tv_sec
#         self._events[self._event_index].time.tv_sec = tv.tv_sec
#         self._events[self._event_index].time.tv_sec = tv.tv_sec
#         self._events[self._event_index].time.tv_sec = tv.tv_sec
#         self._event_index = (self._event_index + 1) % self.LIST_SIZE
#
#         # calculate the jitter and return a new event
#         return self._update()
#
#     # TODO: needs implementation
#     def _update(self):
#        return self._event[self._event_index]


#class EventReaderImpl(JitterImpl):
class EventReaderImpl(AbstractReaderImpl):
    """ Used to abstract the actual implementation """
    pass
