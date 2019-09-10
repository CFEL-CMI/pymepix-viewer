""" desy.flash.EventListener

    :copyright: 2019 DESY
    :license: GPL v3, see http://www.gnu.org/licenses/
"""

from pymepix.processing.FlashID.desy.flash.EventInfo import EventInfo


class EventListener:
    """This is the interface definition for event listeners

    Implement this interface to register at the event-source and become notified.

    WARN: The on_event callback is called from a different thread. So make sure
          you can handle it....
    """

#    @abstractmethod
    def on_event(self, event: EventInfo):
        """Called when-ever a new event-id is available.

        Parameters:
            event(desy.flash.EventInfo.EventInfo): The latest event info
        """
        pass

#    @abstractmethod
    def on_connection_lost(self):
        """Called if we have lost the connection and the will be no more event notifications."""
        pass
