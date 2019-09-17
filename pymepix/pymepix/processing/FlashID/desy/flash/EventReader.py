""" desy.flash.EventReader

The EventReader class wraps the required code to receive event notifications.

    :copyright: 2019 DESY
    :license: GPL v3, see http://www.gnu.org/licenses/
"""

from pymepix.processing.FlashID.desy.flash.EventListener import EventListener
from pymepix.processing.FlashID.desy.flash.EventReaderImpl import EventReaderImpl


#class Singleton(type):
#    _instances = {}
#    def __call__(cls, *args, **kwargs):
#        if cls not in cls._instances:
#            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#        return cls._instances[cls]


class Borg:
    """Used to implement singleton patter"""
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


#class EventReader:
#class EventReader(metaclass=Singleton):
class EventReader(Borg):
    """"This is the event-id reader interface class

        It is implemented as singleton, so it is easy to handle within existing
        code bases. Please note that the notification is not async, so if your
        listener is blocking or delaying the call you will run into trouble.

       Usage:
        Implement you own IEventIDListener
        Register your listener on the reader
        Connect the reader to the source
        Enable notifications

        Now you will receive updated event information

    """

    def __init__(self):
        # try to become a singleton...
        Borg.__init__(self)
        # we use proxy pattern here to hide the actual impl
        # users don't have to know the crap we are doing...
        self.__impl = EventReaderImpl()

    def connect(self, host, port = 58050):
        """ Connect to the event id provider server
        :param host: The hostname of the remote machine
        :param port: The port to use for the connection
        """
        self.__impl.connect(host, port)

    def disconnect(self):
        """ Disconnect the reciving thread """
        self.__impl.disconnect();

    def enable_notifications(self, enable = True):
        """Enables/disable the notification mechanism"""
        self.__impl.notify = enable

    def is_notification_enabled(self):
        """Returns the """
        return self.__impl.notify

    def register(self, listener):
        assert isinstance(listener, EventListener), "Invalid type"
        self.__impl.register_listener(listener)

    def unregister(self, listener):
        assert isinstance(listener, EventListener), "Invalid type"
        self.__impl.unregister_listener(listener)

