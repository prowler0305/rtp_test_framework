# Creating Tests
---
The RTPPY framework uses the Javascript Object Notation (JSON) format to indicate what test is executed and its parameters.
The JSON structure consists of an object containing connection information followed by an array of 1 or more dictionary objects
that specify the test to execute and its parameters.

Below is an outline that can be used for creating a test file.

```json
{
    "connection":
    {...},
    "tests":
    [
      {...},
      {...},
      {...}
    ]
}
```

## Connection Object
The connection parameter object specifies the **lpar**, **ssid**, and **userid** to be used for all the tests specified in the
test array.

#### Example
```json
"connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
```

These connection parameters are required but can be overridden at the [command line level](command-line-options.md).

## Test Structure
Each test can have its own set of parameters and command line overrides. Click on the test type name below to learn
about the test itself and its parameters.

* [Interval Compare](interval-compare.md)
* [Aggregate Compare](aggregate-compare.md)
* [Start/Stop Collection](start-collection.md)
* [RTP SQL Activity Suite App](rtptest.md)
* [Abend Restart](abend-restart.md)
* [Distributed SQL](rtpj-exec.md)
* [Lock Release](lock-release.md)

# Adding to Test Library
---
