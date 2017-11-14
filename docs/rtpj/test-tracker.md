# Test Tracker

The test tracker is a short report printed at the end of the log. It is used to tell you how many tests *passed*, were *skipped*, or *failed*. It also contains the timed *duration* of the test.

When executing a [single file JSON test][sft] the tracker will it as one *test*. Therfore, if multiple [single file JSON test][sft] are passed in as parameters, each will count as one test.

When executing a [JSON test suite][ts] the tracker will count submit each test as though it was specified as a separate argument. Therefore, if only one suite is to be executed, the number of tests executed will be equal to the number of tests specified in the parameter.

### Passed Test Summary

![Passed](/images/test_tracking/Test_Results_Passed.PNG)

### Failed Test Summary

When a test has failed the final test output will contain a "Details" section that will contain additional information
about each failure.  The section will include a list of failed tests, in addition each failed test will contain
information about which statement failed and the cause.

In the example below 4 tests have failed.  The first failed test had problems executing statements 2 and 3 receiving a -601
and -117 SQLCODES respectively.

![Failed](/images/test_tracking/Test_Results_Failed.PNG)

### Skipped Test Summary

If there are no failed tests, but a test was skipped because it could not be executed, the summary will show a __FAILED*__
status.

![Failed](/images/test_tracking/Test_Results_Skipped.PNG)

## When has a test "Passed"

A test is considered passed when all statement in a [single file JSON test][sft] have been executed and the DB2 connection has been closed. If a [threading][threading] parameter is present, the test will only be considered *passed* if all threads complete successfully.

## Why would a test be "Skipped"

A test is skipped when...

- The JSON file can not be read or does not exist
- The JSON file is missing a [__test__][sft] or [__suite__][ts] parameter
- The test is missing a [__connection__](json/single-file-tests/#connection-object) or [__statements__](json/single-file-tests/#statements-array) parameter

## Why would a test have "Failed"

A test can fail when...

- An SQL Error is encountered when executing a statement that is not [expected][expect]
- A result set is returned with different properties than were [expected][expect]
- Errors occur when setting or retrieving [parameters][parms]
- An error occurs when closing the Database Connection


[sft]: json/single-file-tests
[ts]: json/test-suites
[threading]: json/single-file-tests/#threading
[expect]: json/single-file-tests/#expectations
[parms]: json/single-file-tests/#arguments
