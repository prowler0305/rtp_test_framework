# Test Structure
---

A single file test is a JSON file that specifies a __test__ parameter that contains an object with a [connection parameter](#connection-object), a [statements parameter](#statement-object), an *optional* [seed parameter](#generated) and an *optional* [threading parameter](#threading). The following example can be used as a outline for writing single file tests. There is also a [complete example](#complete-example) at the end of this document.

```json
{
  "test": {
    "description": "A test description",
    "connection": {...},
    "statements": [
      {...},
      {...},
      {...}
    ]
  }
}
```

# Description

The `description` string is an optional test parameter that provides a basic textual description of the test.  The description
is currently not used by the framework, but may be used in the future for diagnostic and reporting purposes.

Adding a short textual description of the test or test suite is recommended.

```json
{"description": "A textual description for a test."}
```

# Connection Information
---

## Connection Object

##### Valid Parameters

- ssid
- userid

The connection parameter object specifies the __ssid__ and __userid__ to be used for this test. Each test establishes it's own thread that will be used for all the the statements specified in the [statements array](#statements-array). These connection parameters can be overridden at the [test suite](test-suites) level but must be specified to give the test values to default to.

#### Example

```json
{"connection": {
  "ssid": "D11B",
  "userid": "QADBA01"
}}
```

# Statements
---

## Statements Array

The statement array contains a JSON array of [statement objects](#statement-object) that will be sequentially executed.

```json
{"statements":[
  {...},
  {...},
  {...}
]}
```

## Statement Object

##### Valid Parameters

- text   
- type
- subtype
- expect *optional*
- repeat
- pause
- [args Array](#arguments)

#### Example

```json
{
  "text": "WITH PROCS (name, parms) AS (SELECT NAME, PARM_COUNT FROM SYSIBM.SYSROUTINES) SELECT * FROM PROCS WHERE NAME = ?",
  "type": "PREPARE",
  "subtype": "SELECT",
  "repeat": 100,
  "sleep": 1,
  "args": [
    {
      "value": "ADMIN_EXPLAIN_MAINT",
      "type": "static",
      "datatype": "varchar"
    }
  ]
}
```

## Text

The __text__ parameter specifies the text of the SQL or DDL Statement to be executed. JSON does not allow for multi-line strings so writing in [an editor with line wrapping](https://notepad-plus-plus.org/) and [the ability to unwrap or fold lines](https://sourceforge.net/projects/npp-plugins/files/TextFX/) will help you construct longer statements before copying them into your test. You do not need to include a semicolon at the end of the statement.

## Types

__Type__ specifies how you would like the framework to execute your statement. The following are the valid values for __type__ and a few notes about each.

- *Immediate*
    - Statement is passed to DB2 and immediately executed
    - DB2 may choose to prepare the statement (don't be confused if this is how Detector catches it since it is not 1 to 1 analogous with EXECUTE IMMEDIATE)
    - Parameter markers can not be used, text is static and final
- *Prepare*
    - Statement is prepared and then executed
    - If the [repeat](#repeat) parameter is specified the statement will not be prepared again (This is a good way to mimic real world distributed applications)
- *Callable*
    - Statement is prepared and then executed
    - If the [repeat](#repeat) parameter is specified the statement will not be prepared again
    - Allows use of CALL statements to call stored procedures

## SubTypes

__SubType__ specifies the kind of statement you are executing. Currently, the subtype parameter is not used by the framework. Regardless, subtype should be specified for all statements in case a need arises in the future, such as reporting or logging. Examples of __subtype__ are: *SELECT*, *CREATE*, *INSERT*, *DROP*, etc.

## Expect

__Expect__ specifies an object containing the expected results from the execution of the statement. __Expect__ should be specified to allow the [test tracker]() to accuratly report whether a test achieved a *Passed* or *Failed* status. The following parameters are currently supported:

- sqlerror
    - Only checks errors (negative SQLCODES) not warnings (positive SQLCODES)
    - If an error occurs, the framework will check if that error matches the specified integer and if it does, the test will be considered a success
- columns
    - Checks number of columns returned in a result set
    - Marks the test as failed if number of columns does not match the specified value
- rows
    - Checks number of rows returned in a result set
    - Marks the test as failed if number of rows does not match the specified value
- ignore (true/false)
    - ignores any sql errors and the rows/columns returned for a statement. This is useful if the stmt may fail in some cases but the test
      should not fail, such as when dropping objects.

#### Examples

```json
"expect": {
  "sqlerror": -104
}
```

```json
"expect": {
  "rows": 138,
  "columns": 1
}
```

```json
"expect": {
  "ignore": true,
}
```

## Repeat

The __repeat__ parameter specifies the number of times the framework should execute the statement.

Note that when used on a statement with the __type__ *prepare* or *callable* the statement will only be prepared once. This means that the dynamic SQL's access path will only be determined once.

The __repeat__ parameter also has special interactions with [*incremented*](#incremented) and [*generated*](#generated) argument types.

## Sleep

The __sleep__ parameter specifies the number of seconds to pause the test execution after executing the given statement.

If the sleep parameter is omitted the default is 0 seconds.

# Arguments
---

## Arguments Array

The arguments array contains a JSON array of [argument objects](#argument-object) that will be set to the parameter markers, in the statement, in the order that they appear.

```json
"args":[
  {...},
  {...},
  {...}
]
```

## Argument Object

##### Valid Parameters

- type
- subtype
- datatype
- value
- length
- key

Arguments (__args__) allow you to specify values to be inserted into the parameter markers of the statment. Arguments and parameter markers can only be specified on *prepare* or *callable* __type__ statements.

## Types

Just like statements, arguments have a __type__ parameter. There are three types of parameters and two subtypes.

### Static
For parameters where you want to specify an explicit __value__.
#### Example
```json
{
  "value": "ADMIN_EXPLAIN_MAINT",
  "type": "static",
  "datatype": "varchar"
}
```


### Incremented
For parameters where you want the __datatype__ to increment for every [repetition](#repeat) starting at the given __value__. *Currently only the INTEGER datatype is supported.*
#### Example
```json
{
  "value": 1,
  "type": "incremented",
  "datatype": "integer"
}
```

### Generated
For parameters that you would like randomly generated data of the given __datatype__. If a __value__ parameter is specified it will be ignored and the generated value will be used.

Currently, generation is supported for the following datatypes:

- BIGINT
- BOOLEAN
- CHAR*
- DOUBLE
- FLOAT
- INTEGER
- SMALLINT
- TINYINT
- VARCHAR*

\* *__length__ parameter must be specified or else generated value will be truncated when set*


If a __seed__ value is provided on the __test__ object each execution of the test will generate the same random data. This does not mean that every [repetition](#repeat) of the statement will have the same value generated for it; rather, all [repetitions](#repeat) will produce the same random data every time the test is executed.
#### Example
```json
{
  "type": "generated",
  "datatype": "char",
  "length": 10
}
```

## Subtypes

__Subtype__ only needs to be specified when using Statement Type: *Callable* when calling a stored procedure.

### In

*In* is the implied default for all parameters (even for non *callable* statements). An *in* parameter is expected, by the framework, to provide a value to be set to the corresponding parameter marker.

### Out

*Out* should be specified for [output-only](https://www.ibm.com/support/knowledgecenter/SSEPEK_10.0.0/com.ibm.db2z10.doc.apsg/src/tpc/db2z_parameterlistsp.dita) parameters. The *out* parameter should not specify a __value__. Note that the __length__ parameter does not have to be set in the example. *Out* parameter's returned value will be logged.

#### Example
```json
{
  "type": "static",
  "subtype": "out",
  "datatype": "varchar"
},
```

### InOut

*InOut* should be specified for [input and output](https://www.ibm.com/support/knowledgecenter/SSEPEK_10.0.0/com.ibm.db2z10.doc.apsg/src/tpc/db2z_parameterlistsp.dita) parameters. *InOut* parameters should be used like *In* parameters and follow all the required rules of the parameter's __type__. *InOut* parameter's returned value will be logged.

#### Example

```json
{
  "value": 2,
  "type": "static",
  "subtype": "inout",
  "datatype": "smallint"
}
```

### literal

*literal* is used when certain values are to be inserted directly into the sql statement by the java program.

#### Example

```json
"args": [
  {
    "type": "generated",
    "datatype": "integer",
    "subtype": "literal",
    "key": ":H1"
  }
```

### key

*key* is used only when *literal* is the subtype.  The string designated by the key parameter will be replaced in the SQL statement
by the value indicated in the argument.  This can be static, incremented, or generated parameter.

#### Example

```json
 "statements": [
      {
        "text": "SELECT CREATOR,NAME FROM SYSIBM.SYSTABLES WHERE COLCOUNT < :H1 FETCH FIRST 1 ROWS ONLY",
        "type": "IMMEDIATE",
        "subtype": "SELECT",
        "repeat": 100,
        "args": [
          {
            "type": "generated",
            "datatype": "integer",
            "subtype": "literal",
            "key": ":H1"
          }
        ]
      }
    ]
```

### Max

Sets the maximum number of incremented values for a single argument.  Once the maximum number of values 
has been reached the value will be reset to the original value.

This parameter is designed to support separation of repeating literal values from the "repeat" parameter at the 
statement level.

#### Example 

In the below example the Table literal counter argument will cycle through values (1-10).  This will cause values to 
be inserted into tables (RTPJTB1 - RTPJTB10).  Since the statement is repeated 10 times and in batches of 10, this
will result in 10 rows being inserted into ten tables.

```json
    "text": "INSERT INTO RTPJTB:H1 (id, firstname, lastname, title, salary, resume) VALUES (?, ?, ?, ?, ?, ?)",
    "type": "BATCH",
    "subtype": "INSERT",
    "repeat": 10,
    "batches": 10,
    "args": [
      {
        "type": "incremented",
        "datatype": "integer",
        "subtype": "literal",
        "description": "Table literal counter.",
        "value": 1,
        "key": ":H1",
        "max": 10
      },
```

### Batches 

The batches parameter is only valid when the statement type is "BATCH".  The parameter is used for executing batch statements.
The batches value indicates the number of times a statement should be added to the batch. For example, A statement with a repeat value of 1 and 
a batches value of 10 will cause the statement to be added 10 times and executed during one batch execution.

#### Example

In the below example the statement will be executed 100 times in 10 execution batches.
Since the statement is repeated 10 times and in batches of 10, this will result in 10 rows being inserted into ten tables.

```json
    "text": "INSERT INTO RTPJTB:H1 (id, firstname, lastname, title, salary, resume) VALUES (?, ?, ?, ?, ?, ?)",
    "type": "BATCH",
    "subtype": "INSERT",
    "repeat": 10,
    "batches": 10,
    "args": [
      {
        "type": "incremented",
        "datatype": "integer",
        "subtype": "literal",
        "description": "Table literal counter.",
        "value": 1,
        "key": ":H1",
        "max": 10
      },
```

## DataTypes

__DataType__ specifies the DB2 type of the parameter. Currently, the following datatypes are supported for [*static*](#static) types; [*generated*](#generated) types and [*incremented*](incremented) types only support subsets of this list:

- BIGINT
- BINARY
- BIT
- BLOB
- BOOLEAN
- CHAR
- CLOB
- DATE
- DECIMAL
- DOUBLE
- FLOAT
- INTEGER
- LONGVARBINARY
- LONGVARCHAR
- NULL
- NUMERIC
- REAL
- ROWID
- SMALLINT
- SQLXML
- TIME
- TIMESTAMP
- TINYINT
- VARBINARY
- VARCHAR

## Value

The __value__ parameter allows you to provide values for *static* parameters and starting values for *incrementing* parameters. Note that values like *integer* should not be specified within quotes.

### Length

The __length__ parameter is, currently, only used for *generated* parameters. There is no harm in specifying it for static parameters as it could be used by the framework in the future.

# Multi Threaded Tests
---

## Threading Object

##### Valid Parameters

- threads (integer) : The number of threads to execute test.  Each thread will execute the entire test. One is the default.
- parallel (boolean): Execute all threads in parallel or wait for each thread to finish before starting the next. True is the default.
- sleep (integer)   : The amount of time to wait before executing the next thread.  Zero is the default.

The __threading__ parameter object is used to execute multiple instances of a test either in parallel or sequentially. The __threads__ parameter specifies the number of threads to be created; each thread will have it's own connection. The __parallel__ parameter specifies whether the threads should execute in parallel or sequentially waiting for each to finish before the next is created.

#### Example

```json
"threading": {
  "threads": 100,
  "parallel": "true"
  "sleep": 1
}
```

# Complete Example
---

The following is an example that creates a table, inserts 50 rows to it using all three __type__ of parameters, selects the contents of that table, and drops the table.

```json
{
  "test": {
    "description": "This is an example test file.",
    "seed": 42,
    "threading": {
      "threads": 2,
      "parallel": "false"
    },
    "connection": {
      "ssid": "D10A",
      "userid": "QADBA01"
    },
    "statements": [
      {
        "text": "CREATE TABLE RTPJSONTEST ( id INTEGER, myint INTEGER, mystring VARCHAR(30), mydouble DOUBLE, myfloat FLOAT)",
        "type": "IMMEDIATE",
        "subtype": "CREATE"
      },
      {
        "text": "INSERT INTO RTPJSONTEST (id, myint, mystring, mydouble, myfloat) VALUES (?, ?, ?, ?, ?)",
        "type": "prepare",
        "subtype": "INSERT",
        "repeat": 50,
        "args": [
          {
            "value": 1,
            "type": "incremented",
            "datatype": "integer"
          },
          {
            "type": "generated",
            "datatype": "integer"
          },
          {
            "type": "generated",
            "datatype": "varchar",
            "length": 30
          },
          {
            "type": "generated",
            "datatype": "double"
          },
          {
            "type": "generated",
            "datatype": "float"
          }
        ]
      },
      {
        "text": "SELECT * FROM RTPJSONTEST",
        "type": "IMMEDIATE",
        "subtype": "SELECT",
        "expect": {
          "columns": 5,
          "rows": 50
        }
      },
      {
        "text": "DROP TABLE RTPJSONTEST;",
        "type": "IMMEDIATE",
        "subtype": "DROP"
      }
    ]
  }
}
```

#### Some Notes About this Example

- The __seed__ parameter is set which causes the data to be inserted to be the same every time this test is executed
- The SELECT statement uses the __expect__ parameter to verify that the correct number of columns and rows were returned
- The __threading__ object executes this test twice, on two threads, one after another
- If __parallel__ was set to *true* in the __threading__ object...
    - The CREATE and DROP statements would most likely get sqlerrors on the second thread to execute
    - The SELECT would most likely fail to meet it's __expect__ because the second thread would have inserted more than 50 rows to the table
