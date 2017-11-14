# Suite Structure
---

A test suite is a JSON file that specifies a __suite__ parameter that contains a __tests__ parameter and an *optional* __connection__ parameter. Test suites can only execute tests that are embedded into the JAR, in the `resources/test_library`.

The __tests__ parameter specifies an array of strings representing the names of the [single file tests](single-file-tests) that are to be executed. Tests will be executed one after another.

The connection object specified at the suite level overrides the connection objects in all of the [single file tests](single-file-tests). The [valid parameters and structure](single-file-tests/#connection-object) are identical to the connection object for a [single file test](single-file-tests).

# Description

The `description` string is an optional test parameter that provides a basic understanding of the test.  The description
is currently not used by the framework, but will be used in the future for diagnostic and reporting purposes.

Adding a short textual description of the test or test suite is recommended.

## Example

```json
{
  "suite": {
    "description": "An Example test suite that executes four tests.",
    "connection": {
      "ssid": "DB0G",
      "userid": "QADBA01"
    },
    "tests": [
      "BasicSelectTest.JSON",
      "BasicMultiThreadedSelectTest.JSON",
      "BasicCreateInsertTest.JSON",
      "BasicStoredProcedureTest.JSON"
    ]
  }
}
```
