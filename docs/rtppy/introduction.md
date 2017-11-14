# Welcome

These pages provide information on the python based testing framework which was developed to allow automation testing of
CA Detector, CA Subsystem Analyzer, CA Thread Terminator/DSNZPARM, and CA Xmanager products.

The framework is written in Python and designed to simplify executing, adding, overriding, changing, and writing new tests.
It uses the Prague Testing Gears 2 (PTG2) framework as a base and wrappers simple navigation methods into product based navigation.

The RTP test framework also allows for easy extraction and comparison of metric data collected by the products.

## Executing Tests
Tests can be invoked either remotely via the [Jenkins](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/) website or locally.

Since python is an interpretive language there is nothing special needed to execute the tests locally on your machine other than to perform
the following steps from our [Getting Started](../getting-started.md) page.

* Install PTG2
* Get the RTP project source code

Whether executing the tests via Jenkins or locally see the [Execution](executing-tests.md) page to get started.