# Testing the DRP FFB test system

The data reduction pipeline (DRP) development system was setup in 2018 and is used to develop the DRP 
and understand and test the performance of the system. The dev-DRP consists of 24 client nodes and 
eight data servers that are used as Lustre OSS nodes. All nodes are connected with a single Infiniband
EDR (100Gb) switch.

## FFB Setup 

The FFB system consists of 8 servers each with the following characteristics:

* **storage:** 4x Micron 9200 MTFDHAL3T2TCU nvme-SSDs each with 3.2TB capacity (MAX line)
  * PCIe x4 Gen3
  * sequential read: 3.5GB/s,   sequential writes: 3.1GB/s   (@128KB)
  * random reads: 840K random writes: 285K  (@4KB)
  * endurance: 17.5PB  (5600 writes/cell, filling it up 3 times a day over 5yr)
* **cpu:** 2x Intel Xeon Silver 4114T CPU @ 2.20GHz,  10 cores each, hyperthreading turned on
* **network:** 1x single port EDR Infiniband adapter, MCX455A-ECAT Mellanox MT27700 Family [ConnectX-4], PCIe3.0 x16
* **OS:** RHEL 7.6 
* **filesystem:** Lustre 2.12.0 with zfs 0.7.12-1. 

Each OSS has one OST made up of the four nvme-SSDs formatted with zfs in a raidz1 configuration
(one of the four disks can fail). The zfs recordsize is 1MB (??) and compression and atime are turned off.
The nvme-SSDs use a 4K blocksize. 

Lustre tuning:
TODO:
 
## Terminology

**client** is used for client nodes (machines). Each node might run multiple *processes* which 
are either threads or os-processes.
  
## Write performance of a single node with multiple processes
For details see: [doc](single_writer.md) [notebook](single_client.ipynb)

The write performance of a single using 1-32 processes and writing to multiple osts was measured. 
The short summary is:

* A single process bandwidth is about 1GB/s  (writing to single OST)
* The bandwidth of multiple processes writing to the same OST saturates quickly to about 3GB/s
* The bandwidth writing to all eight OSTs is close to the IB limit (100Gb/s) but requires many 
  processes  

The following figure shows the total bandwidth and the bandwidth per process. The different colors/shapes 
indicate the numbers of OSTs that were used for writing. Each process wrote to one OST and the processes 
were equally spread over the OSTs.

![](pics/single_node_wbw.png)

For some of the tests multiple configurations were used. For example a single process writing to 
a single OST was performed for all OSTs and therefore there are 8 blue triangles in the plots
(some lie on top of each other). The fluctuations are not just due to difference in performance of 
the OST but also due to Lustre caching. For more information see the detail documents above.

## Write performance for many client nodes 
Details: [nodebook](many_writer.ipynb) 

The write bandwidth was tested using:

* multiple nodes with one process per node write to a single OST
* multiple nodes with four processes per node write to all eight OST
  The selection of OSTs were done by lustre.

![](pics/multiple_node_wbw.png)


## Reading while writing
Details: [doc](read_while_write.md)

A single file was written with fio. At the same time reader processes were reading 
from the file written to by fio. If a reader read zero bytes, reaching the end of the 
file, it went to sleep for 100ms. For this test each reader read the whole file (in LCLS
each of the N-readers will read only 1/N of the total bytes, at least to first approximation).

Three test were performed:

\# of reader | rate [MB/s]
----------- | -----------
0 | 993
1 | 800
8 | 928 

A single reader cause a drop in write rate of about 20%. For eight reader the drop was less
than 10% however this might been an artifact of the test setup. All eight readers read the whole
file which might have make them slower than the writing and keeping them away from the end of
the file. A more realistic test would be reading the whole file only once and every reader accesses 
only 1/N'th of the file (assuming N-readers).

The following plot shows the write latency reported by fio showing that in the case of active readers there 
are some writes that are slow. 
![](pics/rww_latency.png)
