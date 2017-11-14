# Running Tests

## The JsonTestRunner Class

The java class com.ca.rtp.core.JsonTestRunner is the main test driver and entry point for the RTPJ framework.  This
class oversees the execution of all tests specified via the command line arguments.  As such the JsonTestRunner
class will be specified on each command used to execute the framework.

## Execute Commands

The following commands can be used to execute tests using the rtpj-1.0-SNAPSHOT.jar file:

    Including CLASSPATH:
    java -cp <class-path-info> com.ca.rtp.core.JsonTestRunner <tests> <options>

    CLASSPATH set previously:
    java com.ca.rtp.core.JsonTestRunner <tests> <options>

*Note: The examples below make use of certain environment variables.  It is recommended that these be setup prior
to executing the jar file. See [Build Instructions - Step 2: Set OS environment variables](build-instructions.md) for details.*

## Setting the CLASSPATH

The CLASSPATH must either be set before or be specified inline as part of the command.

#### Using the -cp command line option:

The -cp command line option can be used to set or modify the current CLASSPATH before execution of the jar.

Example (using environment variables):

    java -cp "%JDBC_DRIVERS%\*";"%RTP_HOME%\rtpj\target\rtpj-1.0-SNAPSHOT.jar" com.ca.rtp.core.JsonTestRunner <tests> <options>

#### Setting the CLASSPATH environment variable:

The CLASSPATH environment variable can be set before executing the jar file.  This has the benefit of making the execution
command much shorter.

##### Windows

    set CLASSPATH=%JDBC_DRIVERS%\*;%RTP_HOME%\rtpj\target\rtpj-1.0-SNAPSHOT.jar;%CLASSPATH%

##### Unix

    export CLASSPATH=$JDBC_DRIVERS\*;%RTP_HOME%\rtpj\target\rtpj-1.0-SNAPSHOT.jar;$CLASSPATH

## Command Line Options

Options are prefixed with `--` and will override default framework behavior.

#### SSID

The SSID to be used for test execution can be overridden using the __SSID__ option.

Example:

    --SSID=D11A

#### LPAR

The LPAR to be used for test execution can be overridden using the __LPAR__ option.  The LPAR option is only
used when the -SSID parameter is also present.

Example:

    --LPAR=CA11

#### USERID

The USERID parameter to be used for test execution can be overridden using the __USERID__ option.

Example:

    --USERID=QADBA01

Order of precedence is as follows: (USERID command line option, Test Suite `Connection` Parameter, Test `Connection` Parameter).

#### LOG

The LOG parameter can be used to override the default log4j2 log level.

    --LOG=OFF
          FATAL
          ERROR
          WARN
          INFO
          DEBUG - Additionally displays framework diagnostic information.
          TRACE - Additionally displays DB2 query output.
          ALL

#### LIBRARY

By default, the framework uses internal library of tests located within the jar.
This can be overridden to specify a different directory to be searched.

Example:

    --LIBRARY=C:\Users\qadba01\mylib\

Inside of the directory `mylib` JSON test files and suites can be placed and referenced as [Test Arguments](#test-arguments).
Currently, the framework does not allow subdirectories in an external library.

## Internal Test Library

The RTPJ framework uses an internal test library for executing most tests.

The Internal Test library is located here: `/rtpj/src/main/resources/test_library`

## Specifying Tests

Test arguments specify the [Test Suites](json/test-suites) and [Single File Tests](json/single-file-tests) to be executed.
Multiple test arguments can be specified; note that [options](#options) apply to all tests in the command.

__Example 1:__ Execute the `Common_Table_Expression_Test.JSON` test from the internal test library.

    java com.ca.rtp.core.JsonTestRunner Common_Table_Expression_Test.JSON

__Example 2:__ Execute the `Basic_Test_Suite.JSON` test suite from the internal test library.

     java com.ca.rtp.core.JsonTestRunner Basic_Test_Suite.JSON

__Example 3:__ Execute the `Basic_Test_Suite.JSON` test suite from the internal test library and override the SSID and USERID values.

     java com.ca.rtp.core.JsonTestRunner Basic_Test_Suite.JSON --SSID=D10A --USERID=<pmfkey>

__Example 4:__ Execute the `Basic_external_test.JSON` test from an external location (example only, not executable).

     java com.ca.rtp.core.JsonTestRunner Basic_external_test.JSON --LIBRARY=C:\Users\<pmfkey>\test_lib

*Note: Examples assume the CLASSPATH was set before command execution.

## Scripts

There are helpful windows batch scripts located here: `rtpj/scripts`

The `run.bat` script can be used to execute the rtpj-1.0-SNAPSHOT.jar file.
The script will set the classpath based on the existing environment variables.

There are two additional variables set in the script, modify these values before executing:

    RTP_TEST=<test file to execute>

    RTP_PARMS=<optional command line test parameters>