import numpy as np
import time

class FakePacket(object):



    def __init__(self,filename):

        self._filename = filename
        self._current_time = 0
        #print('QUEUE',self._output_queue)

        self.openFile()

    def openFile(self):

        self._file = open(self._filename,'rb')
        #Find longtime
        #Read about 8 mb
        buffer = self._file.read(8192*100)
        packet = np.frombuffer(buffer,dtype=np.uint64)
        header = ((packet & 0xF000000000000000) >> 60) & 0xF
        subheader = ((packet & 0x0F00000000000000) >> 56) & 0xF
    


        trigger_header = (header==0x4)|(header==0x6)
        lsb_time_filter =trigger_header & (subheader == 0x4)
        msb_time_filter = trigger_header & (subheader == 0x5)
        lsb = int(packet[lsb_time_filter][0])
        msb = int(packet[msb_time_filter][0])


        #Move it back by one second
        self._current_time = int(self.compute_new_time(lsb,msb)- (1E9//25))
        print(self._current_time*25E-9)

        self._file.seek(0)
        


    def run(self):

        
        buffer = self._file.read(8192*8192) # buffer size is 1024 bytes
        print(len(buffer)/8)
        while buffer:
            out_packet = None

            packet = np.frombuffer(buffer,dtype=np.uint64)
            #self._file_queue.put(('WRITE',raw_packet))
            header = ((packet & 0xF000000000000000) >> 60) & 0xF
            subheader = ((packet & 0x0F00000000000000) >> 56) & 0xF

            trigger_header = (header==0x4)|(header==0x6)
            lsb_time_filter =np.where(trigger_header & (subheader == 0x4))[0]
            msb_time_filter = np.where(trigger_header & (subheader == 0x5))[0]
            #print(msb_time_filter)
            start_index = 0

            if lsb_time_filter.size > 0 and msb_time_filter.size > 0:
                
                for x in range(min(lsb_time_filter.size,msb_time_filter.size)):
                    
                    end_index = msb_time_filter[x]
                    _packet = packet[start_index:end_index]
                    self.upload_packet(_packet)

                    lsb = packet[lsb_time_filter[x]]
                    msb = packet[msb_time_filter[x]]
                    self._current_time = self.compute_new_time(lsb,msb)
                    start_index = end_index
                    #print(self._current_time*25E-9)
                    res= self.upload_packet(packet[start_index:])
                    if out_packet is None:
                        out_packet = res
                    else:
                        out_packet = np.append(out_packet,res)

            else:
                res = self.upload_packet(packet)
                if out_packet is None:
                    out_packet = res
                else:
                    out_packet = np.append(out_packet,res)            
        # self._output_queue.put(None)
            if out_packet is not None:
                yield res
            buffer = self._file.read(8192*8192)

    def upload_packet(self,packet):
        #Get the header
        header = ((packet & 0xF000000000000000) >> 60) & 0xF
        subheader = ((packet & 0x0F00000000000000) >> 56) & 0xF
        pix_filter = (header ==0xA) |(header==0xB) 
        trig_filter =  ((header==0x4)|(header==0x6) & (subheader == 0xF))
        tpx_filter = pix_filter | trig_filter
        tpx_packets = packet[tpx_filter]
        #print(tpx_packets)
        return tpx_packets

    def compute_new_time(self,lsb,msb):
        pixdata = int(lsb)
        longtime_lsb = (pixdata & 0x0000FFFFFFFF0000) >> 16
        pixdata = int(msb)
        longtime_msb = (pixdata & 0x00000000FFFF0000) << 16
        tmplongtime = (longtime_msb | longtime_lsb)
        return tmplongtime

class PacketProcessor(object):

    def __init__(self,exposure_time = None):

        self._col = None
        self._row = None
        self._tot = None
        self._toa = None
        self._exposure_time = exposure_time
        self._triggers = None
        self._trigger_counter = 0

        self._find_time = 0
        self._process_trig_time = 0
        self._process_pix_time = 0
        self._find_event_time = 0

        self._decode_time = 0

        self._append_time = 0

        self._put_time = 0
        self._put_count = 0

        self._find_count= 0
        self._process_trig_count= 0
        self._process_pix_count= 0
        self._find_event_count= 0
        self._append_count = 0



    def reset(self):
        self._longtime_lsb = 0
        self._longtime_msb = 0
        self._longtime = 0

        self._col = None
        self._row = None
        self._tot = None
        self._toa = None

        self._triggers = None
        self._trigger_counter = 0    

    # def process_pixels(self,pixdata,longtime):
    #     dcol        = ((pixdata & 0x0FE0000000000000) >> 52)
    #     spix        = ((pixdata & 0x001F800000000000) >> 45)
    #     pix         = ((pixdata & 0x0000700000000000) >> 44)
    #     col         = (dcol + pix//4)
    #     row         = (spix + (pix & 0x3))


    #     data        = ((pixdata & 0x00000FFFFFFF0000) >> 16)
    #     spidr_time  = (pixdata & 0x000000000000FFFF)
    #     ToA         = ((data & 0x0FFFC000) >> 14 )
    #     ToA_coarse  = (spidr_time << 14) | ToA
    #     FToA        = (data & 0xF)*1.5625E-9
    #     globalToA  =(ToA_coarse)*25.0E-9 - FToA + self._pixel_time


    #     ToT         = ((data & 0x00003FF0) >> 4)*25.0E-9
        

    #     if self._col is None:
    #         self._col = col
    #         self._row = row
    #         self._toa = globalToA
    #         self._tot = ToT
    #     else:
    #         self._col = np.append(self._col,col)
    #         self._row = np.append(self._row,row)
    #         self._toa = np.append(self._toa,globalToA)
    #         self._tot = np.append(self._tot,ToT)

    def process_pixels(self,pixdata,longtime):
        start = time.time()

        dcol        = ((pixdata & 0x0FE0000000000000) >> 52)
        spix        = ((pixdata & 0x001F800000000000) >> 45)
        pix         = ((pixdata & 0x0000700000000000) >> 44)
        col         = (dcol + pix//4)
        row         = (spix + (pix & 0x3))


        data        = ((pixdata & 0x00000FFFFFFF0000) >> 16)
        spidr_time  = (pixdata & 0x000000000000FFFF)
        ToA         = ((data & 0x0FFFC000) >> 14 )
        FToA        = (data & 0xF)
        self._decode_time += time.time()- start
        ToA_coarse  = self.correct_global_time((spidr_time << 14) | ToA,longtime)
        



        ToT         = ((data & 0x00003FF0) >> 4) #Convert to ns


        globalToA = (ToA_coarse << 12) - (FToA << 8)
        globalToA += ((col//2) %16 ) << 8
        globalToA[((col//2) %16)==0] += (16<<8)
        time_unit=25./4096
        finalToA = globalToA*time_unit*1E-9

        ToT *= 25


        self._process_pix_time+= time.time() - start
        self._process_pix_count+=1
        start = time.time()
        #print('PIXEL',finalToA,longtime)
        if self._col is None:
            self._col = col
            self._row = row
            self._toa = finalToA
            self._tot = ToT
        else:
            self._col = np.append(self._col,col)
            self._row = np.append(self._row,row)
            self._toa = np.append(self._toa,finalToA)
            self._tot = np.append(self._tot,ToT)
        self._append_time+= time.time()-start
        self._append_count += 1

    def correct_global_time(self,arr,ltime):
        pixelbits = ( arr >> 28 ) & 0x3
        ltimebits = ( ltime >> 28 ) & 0x3
        diff = ltimebits - pixelbits
        neg = (diff == 1) | (diff == -3)
        pos = (diff == -1) | (diff == 3)
        zero = (diff == 0) | (diff == 2)
        arr[neg] =   ( (ltime - 0x10000000) & 0xFFFFC0000000) | (arr[neg] & 0x3FFFFFFF)
        arr[pos] =   ( (ltime + 0x10000000) & 0xFFFFC0000000) | (arr[pos] & 0x3FFFFFFF)
        arr[zero] = ( (ltime) & 0xFFFFC0000000) | (arr[zero] & 0x3FFFFFFF)
        #arr[zero] =   ( (ltime) & 0xFFFFC0000000) | (arr[zero] & 0x3FFFFFFF)
        
        return arr

    def process_triggers(self,pixdata,longtime):
        start = time.time()
        coarsetime = pixdata >>12 & 0xFFFFFFFF
        coarsetime = self.correct_global_time(coarsetime,longtime)
        tmpfine = (pixdata  >> 5 ) & 0xF
        tmpfine = ((tmpfine-1) << 9) // 12
        trigtime_fine = (pixdata  & 0x0000000000000E00) | (tmpfine & 0x00000000000001FF)
        time_unit=25./4096
        tdc_time = (coarsetime*25E-9 + trigtime_fine*time_unit*1E-9)
        # coarsetime = (pixdata >> 9) & 0x7FFFFFFFF

        # coarsetime >>=3


        # tmpfine = (pixdata >> 5 ) & 0xF
        # tmpfine = ((tmpfine-1) << 9) // 12
        # trigtime_fine = (pixdata & 0x0000000000000E00) | (tmpfine & 0x00000000000001FF)

        # globaltime = self.correct_global_time(coarsetime,longtime)
        # #time_unit=25./4096.0
        # # global_clock = (current_time & 0xFFFFC0000000)*1.5925E-9
        
        # #print('RawTrigger TS: ',coarsetime*3.125E-9 )
        # #Now shift the time to the proper position


        # time_unit=25./4096
        m_trigTime = tdc_time

        self._process_trig_time+= time.time() - start
        self._process_trig_count+=1
        #print('TRIGGERS',m_trigTime,longtime*25E-9)
        start = time.time()
        if self._triggers is None:
            self._triggers = m_trigTime
        else:
            self._triggers = np.append(self._triggers,m_trigTime)
        self._append_time += time.time()-start
        self._append_count+=1
    def updateBuffers(self,val_filter):
        self._col = self._col[val_filter]
        self._row = self._row[val_filter]
        self._toa = self._toa[val_filter]
        self._tot = self._tot[val_filter]

    def getBuffers(self,val_filter):
        return np.copy(self._col[val_filter]),np.copy(self._row[val_filter]),np.copy(self._toa[val_filter]),np.copy(self._tot[val_filter])


    def process_packets(self,packets,longtime):
        packet = packets

        header = ((packet & 0xF000000000000000) >> 60) & 0xF
        subheader = ((packet & 0x0F00000000000000) >> 56) & 0xF

        pixels = packet[np.logical_or(header ==0xA,header==0xB)]
        triggers = packet[np.logical_and(np.logical_or(header==0x4,header==0x6),subheader == 0xF)]

        if pixels.size > 0:
            self.process_pixels(pixels,longtime)
        if triggers.size > 0:
            self.process_triggers(triggers,longtime)
        return self.find_events_fast()

    def filterBadTriggers(self):
        # OToA = np.roll(self._triggers,1)
        # #Make sure the first is the same
        # OToA[0] = self._triggers[0]
        # diff = np.abs(self._triggers - OToA)
        # #print(diff.max())
        # #print('MAX',diff.max())
        # #Find where the difference is larger than 20 seconds
        # diff = np.where(diff > 20.0)[0]
        # if diff.size > 0:
        #     self._triggers = self._triggers[diff[0]:]
        self._triggers = self._triggers[np.argmin(self._triggers):]
        
    def find_events_fast(self):
        if self._triggers is None:
            return None
        self.filterBadTriggers()
        if self._triggers.size < 5:
            return None

        if self._toa is None:
            return None
        if self._toa.size == 0:
            #Clear out the triggers since they have nothing
            return None
        
        start_time = time.time()
        #Get our start/end triggers to get events
        start = self._triggers[0:-1:]
        if start.size ==0:
            return None

        trigger_counter= np.arange(self._trigger_counter,self._trigger_counter+start.size,dtype=np.int)

        self._trigger_counter = trigger_counter[-1]+1

        # end = self._triggers[1:-1:]
        #Get the first and last triggers in pile
        first_trigger = start[0]
        last_trigger = start[-1]
        #Delete useless pixels beyond the trigger
        self.updateBuffers(self._toa  >= first_trigger)
        #grab only pixels we care about
        x,y,toa,tot = self.getBuffers(self._toa < last_trigger)
        self.updateBuffers(self._toa  < last_trigger)

        #print('toa min/max',toa.min(),toa.max())
        #Delete them from the rest of the array
        #self.updateBuffers(self._toa >= last_trigger)
        #Our event filters
        #evt_filter = (toa[None,:] >= start[:,None]) & (toa[None,:] < end[:,None])

        #Get the mapping
        try:
            event_mapping = np.digitize(toa,start)-1
        except Exception as e:
            print(str(e))
            print(toa)
            print(start)
            raise
        event_triggers = self._triggers[:-1:]   
        self._triggers = self._triggers[-1:]

        self._find_event_time+= time.time() - start_time
        self._find_event_count+=1
        #print('Trigger delta',triggers,np.ediff1d(triggers))

        tof = toa-event_triggers[event_mapping]
        event_number = trigger_counter[event_mapping]

        if self._exposure_time is not None:
            exposure_time = self._exposure_time

            exp_filter = tof <= exposure_time

            return event_number[exp_filter],x[exp_filter],y[exp_filter],tof[exp_filter],tot[exp_filter]
        else:
            return event_number,x,y,tof,tot
    
    def run(self,data,longtime):
        #print('GOT DATA')
        events = self.process_packets(data,longtime)

        if events is not None and self._output_queue is not None:
            return events
        else:
            return None

class TimepixCentroid(object):

    def __init__(self):
        pass
    def compute_blob(self,shot,x,y,tof,tot):
        start = time.time()
        labels = self.find_cluster(shot,x,y,tof,tot,epsilon=2,min_samples=5)

        label_filter = labels!=0
        if labels is None:
            return None
        if labels[label_filter ].size ==0:
            return None
        else:
            start = time.time()
            props = self.cluster_properties(shot[label_filter ],x[label_filter ],y[label_filter ],tof[label_filter ],tot[label_filter ],labels[label_filter ])
            return props





    def moments_com(self,X,Y,tot):

        total = tot.sum()
        x_bar = (X*tot).sum()/total
        y_bar = (Y*tot).sum()/total
        area = tot.size
        x_cm = X - x_bar
        y_cm = Y - y_bar
        coords = np.vstack([x_cm, y_cm])
        
        cov = np.cov(coords)
        try:

            evals, evecs = np.linalg.eig(cov)
        except:
            evals = np.array([0.0,0.0])
            evecs = np.array([[0.0,0.0],[0.0,0.0]])


        return x_bar,y_bar,area,total,evals,evecs.flatten()

    def find_cluster(self,shot,x,y,tof,tot,epsilon=2,min_samples=2,tof_epsilon=None):
        from sklearn.cluster import DBSCAN
        
        if shot.size == 0:
            return None
        #print(shot.size)
        tof_eps = 81920*(25./4096)*1E-9/5.0


        tof_scale = epsilon/tof_eps
        X = np.vstack((shot*epsilon*1000,x,y,tof*tof_scale)).transpose()
        dist= DBSCAN(eps=epsilon, min_samples=min_samples,metric='euclidean',n_jobs=1).fit(X)
        labels = dist.labels_ + 1
        return labels

    def cluster_properties(self,shot,x,y,tof,tot,labels):
        label_iter = np.unique(labels)
        total_objects = label_iter.size


        #Prepare our output
        cluster_shot = np.ndarray(shape=(total_objects,),dtype=np.int)
        cluster_x = np.ndarray(shape=(total_objects,),dtype=np.float64)
        cluster_y = np.ndarray(shape=(total_objects,),dtype=np.float64)
        cluster_eig = np.ndarray(shape=(total_objects,2,),dtype=np.float64)
        cluster_vect = np.ndarray(shape=(total_objects,4,),dtype=np.float64)
        cluster_area = np.ndarray(shape=(total_objects,),dtype=np.float64)
        cluster_integral = np.ndarray(shape=(total_objects,),dtype=np.float64)
        cluster_tof = np.ndarray(shape=(total_objects,),dtype=np.float64)
        

        for idx in range(total_objects):


            obj_slice = (labels == label_iter[idx])
            obj_shot = shot[obj_slice]
            #print(obj_shot.size)
            obj_x = x[obj_slice]
            obj_y = y[obj_slice]
            obj_tof = tof[obj_slice]
            obj_tot = tot[obj_slice]
            max_tot = np.argmax(obj_tot)

            cluster_tof[idx] = obj_tof[max_tot]
            


            x_bar,y_bar,area,integral,evals,evecs = self.moments_com(obj_x,obj_y,obj_tot)
            cluster_x[idx] = x_bar
            cluster_y[idx] = y_bar
            cluster_area[idx] = area
            cluster_integral[idx] = integral
            cluster_eig[idx]=evals
            cluster_vect[idx] = evecs
            cluster_shot[idx] = obj_shot[0]



            # moment = moments(obj_x,obj_y,obj_tot)
            # moments_com(obj_x,obj_y,obj_tot)
            #print(moment)
            # gauss = fitgaussian(obj_x,obj_y,obj_tot)
            # gh,gx,gy,gwx,gwy = gauss
            # cluster_h[idx] = gh
            # cluster_x[idx] = gx
            # cluster_y[idx] = gy
            # cluster_wx[idx] = gwx
            # cluster_wy[idx] = gwy
            # cluster_shot[idx] = obj_shot[0]

            #print('Moment ', moment,' Gaussian ',gauss)

        return cluster_shot,cluster_x,cluster_y,cluster_area,cluster_integral,cluster_eig,cluster_vect,cluster_tof    

    
    def run(self,events):
        blob_data = self.compute_blob(*events)

        return blob_data



def compute_blobs(filename,exposure):
    packet = FakePacket(filename)
    event = PacketProcessor(exposure)
    blob = TimepixCentroid()

    for p in packet.run():
        print(p)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Helper client for pixel clustering')
    parser.add_argument("-f", "--filename",dest='filename',type=str, required=True)
    parser.add_argument("-e", "--exposure",dest='exposure',default=10.0,type=float)

    args = parser.parse_args()

    compute_blobs(args.filename,args.exposure)


if __name__=="__main__":
    main()