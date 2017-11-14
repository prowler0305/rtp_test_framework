# Test Automation Framework Project
This repository contains the project source for the Python based test automation framework (rtppy) that I designed and implemented and serves as an example of my knowledge and skills as a software engineer.

You can view documentation that explains the high level architecture [here](https://prowler0305.github.io/andrew-spear-personal/rtppy/automation_architecture/)

The code is located in the rtppy directory and from there is organized as follows.

* **core** - contains test framework functionality for input parsing, product navigation, data extraction and containment, and other high level functionality organized into both composite and inheritable class objects.
* **pdt_tests**/**psa_tests** - contains all the high level scripts that were used for the product CA Detector which consumed the framework pieces.
* **python_test_library** - contains all the interface JSON files which were the main interface to execute the tests.
* **rtpj_tests** - contained a high level script that used framework functionality that allowed my product team to execute distributed SQL against DB2 using our homegrown Java based framework, RTPJ. This high level test script allowed team members to embedded the execution of distributed SQL into their tests via RTPJ specific JSON files that were kept in a different directory or on their local machine as text files.
* **rtptest_tests** - Contained scripts that allowed interaction of an on mainframe application that I wrote that, just like the RTPJ framework mentioned above, simplified the ability to execute SQL via both CAF and RRSAF DB2 connections. This mainframe framework, named RTPTEST, had options that allowed the test environment to be created and torn down by automating the processes of creating objects, bind of DB2 SQL programs and plans (written in C by team members), execution of said programs, freeing of packages and plans, and deleting of objects into simple to use selectable options. This set of test scripts allows the functions of that application to be embedded into test flows.
* **speantest** - This is where the main driver, ISPFTest.py, is located which the main executable that is called. From there the entire direction is determined by the JSON file which is specified by the command line argument --file.
