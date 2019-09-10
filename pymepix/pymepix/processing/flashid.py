from pymepix.processing.datatypes import MessageType
from pymepix.processing.basepipeline import BasePipelineObject

from pymepix.processing.FlashID.desy.flash.EventListener import EventListener
from pymepix.processing.FlashID.desy.flash.EventReader import EventReader

class FlashIDListener(EventListener, BasePipelineObject):
#class FlashIDListener(BasePipelineObject):
    """Simple implementation of a EventListener interface"""

    def __init__(self,
                 input_queue=None,
                 create_output=True,
                 num_outputs=1,
                 shared_output=None):
        BasePipelineObject.__init__(self, FlashIDListener.__name__,
                                    input_queue=input_queue,
                                    create_output=create_output,
                                    num_outputs=num_outputs,
                                    shared_output=shared_output)
        self.info('Initializing Flash bunch ID listener')

        self.reader = EventReader()
        self.reader.register(self)

        # connect to the event source
        self.info("Flash bunch ID connecting...")
        self.reader.connect("hasfcpuexp2.desy.de")

        self.startGetIDs()

    def on_event(self, event):
        #print(f"Got new event {event.id} {event.time.tv_sec} {event.time.tv_usec}")
        self.debug(f"Got new event {event.id} {event.time.tv_sec} {event.time.tv_usec}")
        self.process(MessageType.FlashData, event)

    def on_connection_lost(self):
        print(f"Disconnected")

    def process(self, data_type=None, event=None):
        if data_type is not MessageType.FlashData or event is None:
            return None, None

        #self.info("process FlashID")
        #print('flashidlistener', event)
        data = (event.id, event.time.tv_sec, event.time.tv_usec)
        print(data)
        self.pushOutput(MessageType.FlashData, data)
        #return MessageType.FlashData, event


    def startGetIDs(self):
        # enable notifications
        self.reader.enable_notifications()

    def stopGetIDs(self):
        # disable notifications
        self.reader.enable_notifications(False)



def main():
    import time
    a = FlashIDListener()
    print('Start')
    a.start()
    time.sleep(5)
    print('Pause')
    a.stop()
    print('Start again')
    a.start()
    time.sleep(2)
    print('Stop')
    a.stop()


if __name__ == "__main__":
    main()
