
To install AFL++ on Ubuntu, you can use the following commands:
```
sudo apt update
sudo apt install afl++
``` 

To build Fuzzgoat with afl-clang-fast, run:
```
cd fuzzgoat
CC=afl-clang-fast CXX=afl-clang-fast++ make
```

To run Fuzzgoat with an input file, use:
```
./fuzzgoat input.txt
```

To start fuzzing with AFL++, use:
```
export AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1
afl-fuzz -i seeds -o findings -- ./fuzzgoat @@
```

To debug a crash found by AFL++, use gdb as follows:
```
gdb ./fuzzgoat
(gdb) run < findings/crashes/id:000012*
(gdb) bt
```


Welcome to Fuzzgoat
===================

This C program has been deliberately backdoored with several memory corruption bugs to test the efficacy of fuzzers and other analysis tools. Each vulnerability is clearly commented in fuzzgoat.c. Under input-files/ are files to trigger each vulnerability.

CAUTION: Do not copy any of this code - there is evil stuff in this repo.


Install AFL (American Fuzzy Lop)
------------------------

While Fuzzgoat can be attacked using any fuzzer, we like AFL. To install it:

1. Download AFL: [http://lcamtuf.coredump.cx/afl/releases/afl-latest.tgz](http://lcamtuf.coredump.cx/afl/releases/afl-latest.tgz)

2. Build AFL with `make install`

3. See the AFL quick start guide for more info: [http://lcamtuf.coredump.cx/afl/QuickStartGuide.txt](http://lcamtuf.coredump.cx/afl/QuickStartGuide.txt) 


Building Fuzzgoat
----------

Fuzzgoat builds with make. With afl-gcc in your PATH:

`make`


Running AFL
--------------------------

With afl-fuzz in your PATH and a seed file in a directory called in/

`afl-fuzz -i in -o out ./fuzzgoat @@` 

or simply:

`make afl`

or use the .sh
`./run_afl_parallel.sh ./fuzzgoat ./in ./out 5`
to monitor the state:
`afl-whatsup ./out`

[*] 所有 fuzzer 都已在背景啟動。
    你可以用 'ps aux | grep afl-fuzz' 看目前狀態
    或直接用 'afl-whatsup $OUTPUT_DIR' 查看整體 coverage/速率。

[*] logs/ 底下有各 instance 的 log：
    ls logs/
[*] 要結束的話，直接 kill 這些 afl-fuzz process，或用:
    pkill -f afl-fuzz



Thank You
---------
Contributor: Joseph Carlos 

Fuzzgoat was adapted from udp/json-parser - we chose it because:

* Its not too big or cumbersome - ~1200 lines of C yet lots of paths for a fuzzer to dig into.
* Performance: its very fast at ~1500 execs per sec per core.
* The code is clean and very readable.

Fuzz Stati0n would like to thank the creators and maintainers of udp/json-parser. 
