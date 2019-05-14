# Write Performance of a single client node

For the system setup see [Setup](README.md).

The performance of a single client node was tested using multiple processes writing
to a single or multiple osts. All test were performed with _fio_.

Some results are shown in the notebook: 
    
- [Single Writer](single_client.ipynb)


## Writing a single file to a single OS

A sequence of test writing to one OST at a time was performed. For each test a 200 GiB 
file was written (over written if it already existed). For the first test group the OSTs
were written in the following order:

> OST write order: 1 2 3 4 5 6 7 8 1 2 3 4 5 6 8 

![](pics/single_writer_20190427T214052_ib.png)
![](pics/single_writer_20190427T214052_cache.png)

The second test group used a random order:

> OST write order: 7 8 1 4 5 1 5 4 8 7

The zfs write rate, cpu usage an cache usage are shown in the foloowing plot.

![](pics/single_writer_20190428T081321_ib.png "ZFS write rate repeated osts selection")
![](pics/single_writer_20190428T081321_cache.png "cpu-load abd cache usage repeated osts selection")

Once the cache usage hits the maximum (~81GB a Lustre setting) the performance 
starts to drop. In the random case the drop is not as prevalent as in the 
ordered case. 

## Random and direct IO

Four tests were performed each writing a 200GiB file to OST-8: 

1. sequential write, buffered IO
2. random write, buffered IO
3. sequential writes with direct IO
4. random writes, direct IO

The plots below show the zfs write rate, IB bandwith on the OSS and cpu and
cache usage on the client node.

* For buffer random IO the bandwidth drops slightly compared to the sequential 
  write case. 
* Direct IO shows poor performance (about 5x slower) compared to buffered IO. 
* The ratio of IB-bandwith / zfs-bandwith is much smaller compared to the 
  expected one due to raidz (3/4). Increasing the write block size improves 
  the ratio as shown in the following table: 

bs [MiB]| IB/zfs | IB [MiB/s] | zfs [Mib/s] 
------- | ------ | -----------| ----------- 
1 | 0.38 | 200 |  522 
4 | 0.61 | 580 |  959 
8 | 0.67 | 805 | 1201
16 | 0.71 | 969 | 1369 

  For buffer IO the ratio is close to the expected one. 

![](pics/single_writer_rnd_direct_write_IO.png)
![](pics/single_writer_rnd_direct_write_cache.png)

