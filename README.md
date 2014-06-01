Bongger integration/staging tree
================================

http://www.bongger.com

Copyright (c) 2009-2013 Bitcoin Developers
Copyright (c) 2011-2013 Litecoin Developers
Copyright (c) 2011-2014 Bongger Developers

What is Bongger?
----------------

Bongger is a lite version of Bitcoin using scrypt as a proof-of-work algorithm.

    Algo:  Scrypt
    RPC Port: 7070
    P2P Port: 7071 
    Rewards per block: 420 Coins 
    Target per block: 42 Seconds  
    Halving: Every 500,001 Blocks 
    Total Number of Coins: 504,000,000 
    84,000,000 Coins premine to distributed to users,miners and as bounties! 
    420,000,000 Coins left for mining
    block confirmations:  3

For more information, as well as an immediately useable, binary version of
the Bongger client sofware, see http://www.bongger.com.

License
-------

Bongger is released under the terms of the MIT license. See `COPYING` for more
information or see http://opensource.org/licenses/MIT.

Development process
-------------------

Developers work in their own trees, then submit pull requests when they think
their feature or bug fix is ready.

If it is a simple/trivial/non-controversial change, then one of the Bongger
development team members simply pulls it.

If it is a *more complicated or potentially controversial* change, then the patch
submitter will be asked to start a discussion (if they haven't already) on the
[mailing list](http://sourceforge.net/mailarchive/forum.php?forum_name=bitcoin-development).

The patch will be accepted if there is broad consensus that it is a good thing.
Developers should expect to rework and resubmit patches if the code doesn't
match the project's coding conventions (see `doc/coding.txt`) or are
controversial.

The `master` branch is regularly built and tested, but is not guaranteed to be
completely stable. [Tags](https://github.com/bitcoin/bitcoin/tags) are created
regularly to indicate new official, stable release versions of Bongger.

Testing
-------

Testing and code review is the bottleneck for development; we get more pull
requests than we can review and test. Please be patient and help out, and
remember this is a security-critical project where any mistake might cost people
lots of money.

### Automated Testing

Developers are strongly encouraged to write unit tests for new code, and to
submit new unit tests for old code.

Unit tests for the core code are in `src/test/`. To compile and run them:

    cd src; make -f makefile.unix test

Unit tests for the GUI code are in `src/qt/test/`. To compile and run them:

    qmake BITCOIN_QT_TEST=1 -o Makefile.test bongger-qt.pro
    make -f Makefile.test
    ./Bongger-qt_test

