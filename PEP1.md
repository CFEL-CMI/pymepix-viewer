# Abstract
In the current implementation of the Pymepix library, the data pipeline for the individual processes is designed to work with multiprocessing.Qeueu. The data put into the queue is tagged. The processes take data from the queue check the flag and in case that is wrong write the data back to the queue. This makes the design of the queue very flexible and it's very easy to add an additional processing step in any part of the pipeline. This flexibility, however, comes at the cost of performance. Here we propose to re-implement the pipeline optimised for performance rather than flexibility.

# Current Layout
The current design of pymepixs data pipeline makes use of multiprocessing.Queue where all processing steps share the same queue. This only works with the data written into the queue being tagged. Each process takes data from the queue, checks for the flag and in case of the wrong tag, writes it back in the queue. The flexibility of this approach comes at the great cost of performance. One for the fact that in the worst case the same data needs to be written to the queue multiple times and secondly due to the fact that Queue is not the fastest way of sharing between processes.

- write some dummy code simulating the data put into the queue and take it out
- UML flow diagram?
- add code snipped where the tag is being checked
- what's the matter with the input and output queue in the processing classes?
- Queue benchmarks?
- use case provided in the paper for this approach

# New pipeline design
It is questionable if the flexibility provided by the current framework is required. From the experience in the past, we need the flexibility more like in the scalability of the processing power rather than in the layout of the processing pipeline.
- compare runtime multi bunch and single bunch data (events per second)

For TimePix3 we can get a maximum 80MPixel/s what corresponds to 640MByte/s. The expected data rate with TimePix4 this will increase to approximately ???. In light of these data rates and the fact that in particular, the centroiding is very CPU intensive, the new design of the pipeline should be optimised for speed.
To achieve this the proposed approach is to convert pymepix from multiprocessing.Queue to zeroMQ.
- some facts and details about zeroMQ
- how does ZeroMQ compare with other libraries like rabbitMQ or kafka

With this approach, it is easily possible to scale the processing from a single workstation to a distributed cluster /or cloud?/.
- what needs to be changed in the code
- provide code snippet of an example implementation of how this could look like?
- approximate effort?

XFEL already has a data pipeline library implemented which they just want to use with the pymepix library. To get the maximum benefit from collaboration on both sides this requires to further disentangle data pipeline from processing logic. 