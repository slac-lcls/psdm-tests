# Reading while writing 

## Tests

A 200 GiB file was written using: 

> fio --size=200Gi --numjobs=1 --rw=write --ioengine=psync --bs=1Mi --fallocate=none --name rww --directory /ffb01/wktst/tests/s1o2

which creates the /ffb01/wktst/tests/s1o2/rww.0.0. On client nodes different from
the writer the read command was launched:

> $PWD/tst_reader_FILE  /ffb01/wktst/tests/s1o2/rww.0.0 100

The Readers were launched using: *pdsh -w drp-tst-dev0[10-17] $PWD/test_reader_FILE...* .
The second argument is the milliseconds to wait in case zero bytes were read.

### Single Reader

![](pics/read_while_write_w1_r1_grafana.png)


### Eight Readers

Rates reported by the reader executable.

elapsed [mus] | rate [MiB/s
------------- | -----------
317546287 | 676
317554073 | 676
317551316 | 676
317555236 | 676
317552269 | 676
317554014 | 676
317554807 | 676
317552329 | 676

Comments:

- at some moment data have to be read from storage (zfs-read-rate)
- the zfs read rate is less than 1GB/s much smaller than the IB rate 
  so most of the data are read from memory.
- There are some spikes of ~8GB/s reads but mostly it is in the order of 5GB/s.
  All clients read the whole file could it be that the rate gets limited as 
  the clients get synchronized on ssd reads (TODO:).
- The clients should really read disjoint blocks of the file. Right now the clients
  aggregate read is eight times larger than the file size (TODO:).

![](pics/read_while_write_w1_r8_grafana.png)
