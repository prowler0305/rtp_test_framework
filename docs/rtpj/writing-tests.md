# Writing Tests

The RTPJ framework uses the Javascript Object Notation (JSON) format to express a test or test suite.
If you are not familiar with JSON the official documentation is located here: <http://www.json.org/>.

See the following pages for details regarding the test and test suite formats.

[Single File Tests](json/single-file-tests.md)

[Test Suites](json/test-suites.md)

## Test Library

The internal test library is located here: `/rtpj/src/main/resources/test_library`. This directory contains all the
existing tests and is a good place to look for examples to help in writing new tests.

When a test is executed the entire test library including all sub-directories will be searched.
When a test suite is executed the entire test library including all sub-directories will be searched, the entire
test library will then also be searched for each test within the test suite.

All the tests located within the test library are packaged into the **rtpj-1.0-SNAPSHOT.jar** during the build.

This has many benefits:

1.) The tests can be read directly from the .jar file, and are always in the same relative location.

2.) The commands used to execute tests remain simple.

3.) The tests are part of the project source control and build process.

4.) The package has fewer external dependencies.

## Adding a Test

Once you have written a new test and it is ready to be added to the permanent internal test library, simply copy the
JSON file to the following location: `/rtpj/src/main/resources/test_library`.

Once a test file is located within the internal test library directory it can be executed simply by adding the name to the
command line parm list.

The framework will search the library for the test name and execute it.

The entire test library including all sub-directories will be searched for each test.

***Note: duplicate tests names may cause undesired results.***

## Adding a Test Suite

Test Suites are added in the same manner as a Test.  Simply copy the test suite JSON file into the internal
test library directory.

The test library will be searched to locate the test suite file and execute it.  All tests defined within the
test suite must be located within the internal test library.

The entire test library including all sub-directories will be searched for each test within a test suite.

