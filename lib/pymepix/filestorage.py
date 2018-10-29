import multiprocessing

from multiprocessing.sharedctypes import RawArray 
import numpy as np
import socket
import time,os
from multiprocessing import Queue
class FileStorage(multiprocessing.Process):

    def __init__(self,data_queue,file_status):
        multiprocessing.Process.__init__(self)
        self._input_queue = data_queue
        self._file_io = None
        self._raw_file_io = None
        self._blob_file_io = None
    def run(self):

        while True:
            try:
                # get a new message
                packet = self._input_queue.get()
                # this is the 'TERM' signal
                if packet is None:
                    break

                message = packet[0]
                # print(packet)
                #Check signal type
                if message == 'OPEN':
                    path = packet[1]
                    prefix = packet[2]
                    #tof_filename = os.path.join(path,prefix)+time.strftime("%Y%m%d-%H%M%S")+'.dat'
                    raw_filename = os.path.join(path,'raw_'+prefix)+time.strftime("%Y%m%d-%H%M%S")+'.dat'
                    blob_filename = os.path.join(path,'blob_'+prefix)+time.strftime("%Y%m%d-%H%M%S")+'.dat'
                    print('Opening filenames ',blob_filename,raw_filename)
                    if self._blob_file_io is not None:
                        self._blob_file_io.close()
                    if self._raw_file_io is not None:
                        self._raw_file_io.close()
                    
                    #self._file_io = open(tof_filename,'wb')
                    self._raw_file_io = open(raw_filename,'wb')
                    self._blob_file_io = open(blob_filename,'wb')
                elif message == 'WRITE':
                    data = packet[1]
                    #print(packet)
                    if self._raw_file_io is not None:
                        self._raw_file_io.write(data)
                elif message == 'WRITETOF':
                    counter,x,y,tof,tot = packet[1]
                    
                    #print(packet)
                    if self._file_io is not None:
                        np.save(self._file_io,counter)  
                        np.save(self._file_io,x) 
                        np.save(self._file_io,y) 
                        np.save(self._file_io,tof) 
                        np.save(self._file_io,tot)     
                elif message == 'WRITEBLOB':
                    cluster_shot,cluster_x,cluster_y,cluster_area,cluster_integral,cluster_eig,cluster_vect,cluster_tof = data = packet[1]
                    
                    #print(packet)
                    if self._blob_file_io is not None:
                        np.save(self._blob_file_io,cluster_shot)  
                        np.save(self._blob_file_io,cluster_x)
                        np.save(self._blob_file_io,cluster_y)
                        np.save(self._blob_file_io,cluster_area)
                        np.save(self._blob_file_io,cluster_integral)
                        np.save(self._blob_file_io,cluster_eig)
                        np.save(self._blob_file_io,cluster_vect)
                        np.save(self._blob_file_io,cluster_tof)
             
                elif message == 'CLOSE':
                    if self._file_io is not None:
                        self._file_io.close()
                    if self._raw_file_io is not None:
                        self._raw_file_io.close()
                    if self._blob_file_io is not None:
                        self._blob_file_io.close()

                    self._blob_file_io = None
                    self._file_io = None
                    self._raw_file_io = None
            except Exception as e:
                print(str(e))
            
        

