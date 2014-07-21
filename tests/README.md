This directory contains unit tests for the various ciphers and hash functions contained in this repository. These tests mainly assure that the implementations match the test vectors as specified in the design papers, but may sometimes include additional vectors to test specific functions in more detail.

These tests can be conveniently executed using the [nose package](https://nose.readthedocs.org/en/latest/). By executing `nosetests` from the root of this repository, all imports should evaluate correctly without adjusting your `PYTHONPATH`. 
