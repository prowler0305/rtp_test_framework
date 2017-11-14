# JSON parameters
---
Below is the complete list of parameters that can be specified in a JSON file. View the documentation for the
[test](creating-tests.md#test-structure) to find out what parameters are valid.

## Connection object parameters
---

### lpar
The LPAR in which to connect to.

```json
"lpar": "ca31"
```

### userid
The ID to use to log onto the LPAR.

```json
"userid": "qartp01"
```

### ssid
The primary SSID to be used for test execution.

```json
"ssid": "d12a"
```

### ssid2
A second ssid to use during test execution. Refer to the documentation for the specific test as to its meaning and use.

```json
"ssid2": "d11a"
```

## Test object parameters
---

### description
Can be provided to give a description about a test. The occurrence of the description parameter also provides content for the [print](command-line-options.md#print) command line option functionality to print the description to the console for you without having to open the JSON file to see it.

```json
"description": "description about a this test"
```

Example in a JSON file:
```json
 "tests":
  [
    {
      "description": "Compares all the data for an interval between a baseline and a current run for the view_by option display specified.",
      "test_type": "interval compare",
      ...
    }
  ]
```

### product_code
Identifies the product the test is for using the 3 character product code. (e.g. PDT, PSA, PTT, etc...)

```json
"product_code": "PDT"
```

### baseline_vcat
Identifies the VCAT name to be used to identify the baseline datastore to use.

```json
"baseline_vcat": "PDTDBA.QATEST"
```

### baseline_datastore
Identifies the datastore that should be considered to contain the baseline execution metrics.

```json
"baseline_datastore": "BASEDS"
```

### current_vcat
Identifies the VCAT name to be used to identify the current datastore to use.

```json
"current_vcat": "PDTDBA.R19"
```

### current_datastore
Identifies the datastore that should be considered to contain the current execution metrics to compare against the baseline.

```json
"current_datastore": "QATEST"
```
### baseline_interval_date/current_interval_date
Identifies the interval, by date, in the datastore that should be selected in combination with the corresponding
interval_time parameter below.

#### Format
The interval date can be supplied as it appears on the products "Datastore Interval Summary Display" or a value string
of "1" can be used to indicate the most recent interval should be selected.

Using **16/05/13**:

```json
"baseline_interval_date": "16/05/13"
"current_interval_date": "16/05/13"
```
**OR**
```json
"baseline_interval_date": "1"
"current_interval_date": "1"
```

### baseline_interval_time/current_interval_time
Further identifies the interval, by time, in the datastore that should be selected in combination with the corresponding
interval_date parameter specified above. Unless the interval date parameter indicates the most recent interval should be
selected, in which the interval time parameter is ignored.

#### Format
The interval time should be supplied as it appears on the products "Datastore Interval Summary Display".

Using **02:00:00**:

```json
"baseline_interval_time": "02:00:00"
"current_interval_time": "02:00:00"
```

### baseline_interval_date_2/current_interval_date_2
Used to indicate a range of intervals should be selected by identifying a second interval, by date, in the datastore that should be selected in combination with the corresponding interval_time_2 parameter below.

```json
"baseline_interval_date_2": "16/05/13"
"current_interval_date_2": "16/05/13"
```
**OR**
```json
"baseline_interval_date_2": "1"
"current_interval_date_2": "1"
```

### baseline_interval_time_2/current_interval_time_2
Further identifies the second interval that should be selected, by time, in the datastore that should be selected with the corresponding interval_date_2 parameter above when requesting a range of intervals to be selected. If the interval_date_2 parameter indicates the most recent interval should be selected, then the interval_time_2 parameter is ignored.

```json
"baseline_interval_time_2": "02:00:00"
"current_interval_time_2": "02:00:00"
```

### view_type
Indicates what type of data displays to navigate to. (i.e. Standard Activity, Exceptions, Errors, etc...)

```json
"view_type": "X"
```

### view_by
Indicates what Summary Display panel to navigate to.

```json
"view_by": "S"
```

### view_option
Indicates what additional Summary Display panel to navigate to within certain displays in Subsystem Analyzer.

```json
"view_option": "C"
```

### environment
Indicates the release environment of the products to use. This parameter overrides the frameworks default of **R19**.

```json
"environment": "DV19"
```
#### Entering via DB.ALL
To enter into the products using the "Extended General Selection Menu", i.e. DB.ALL, using an overriding parmlib and/or suffix.
Simply specify the overriding parmlib and optionally a suffix in **()**.

Example:
```json
"environment": "MY.OVERRIDE.PARMLIB(99)"
```
### range_pct
Indicates allowable plus or minus range percentage the comparison can be between. This parameter can override a tests default value.

```json
"range_pct": 15
```

### column
Can be used to specify a specific column name for a test to use. The use of the column name can be different for each type of test.
Refer to the documentation for the specific test as to its meaning and use.

```json
"column": "INDB2_TIME"
```

### line_command
Indicates the single character line command option to be used on a display row.

```json
"line_command": "G"
```

### level
Indicates to what level data should be aggregated for during an aggregation comparison. Valid values are **plan**, **program**, or **keys**.

* plan - indicates that the program statistics should be aggregated and compared to the plan level.
* program - indicates that the statement statistics should be aggregated and compared to the program level.
* keys - indicates that the aggregation should be between a key summary display, which is based on the optional **key_option** parameter provided, and
either a "**Key Planname Display**" or a "**Key Package Display**"
* dbase - indicates that the Table Activity data statistics should be aggregated and compared to the Database level.

```json
"level": "plan"
"level": "program"
"level": "keys"
```

### key_option
Specifies the single character that is to be used in the "Key" field on the standard activity Key Summary Display.

```json
"key_option": "R"
```

### key_value
Indicates the value for the "Key" column on the standard activity Key Summary Display or the keyword "ALL" which indicates to some tests that all the Key rows on the display should be selected.

```json
"key_value": "SPEAN03"
```

### plan
Specifies a value that can be used to identify a row on a Planname Display or the keyword "ALL" which can indicate to some tests that all the Plans should be selected.

```json
"plan": "RTPPLNMN"
```
Or

```json
"plan": "ALL"
```

### program
Specifies a value that can be used to identify a row on a Program Display or the keyword "ALL" which can indicate to some tests that all the Programs should be selected.

```json
"program": "REG133DR"
```

Or

```json
"program": "ALL"
```

### collid
Specifies a value that can be used to identify a row on a display that contains the "COLLID" column.

```json
"collid": "RTPCOLMN"
```

### dbname
Specifies a value that can be used to identify a row on the Database Activity Display or the keyword "ALL" which indicates that all the Databases should be selected.

```json
"dbname": "SEGMDB"
```
Or

```json
"dbname": "ALL"
```

### output_location
Indicates that all output should be written to the specified directory location.

**Executing via Locally -** the directory can be any valid path on your local machine and the directory and file will be
 created for you automatically.

**Executing via Jenkins -** This parameter should not be altered.

```json
"output_location": "C:\Users\spean03\Desktop\output"
```

### options
Can be used to contain an array of additional JSON parameters defined within a test. The use of the options parameter can be different for each type of test.
Refer to the documentation for the specific test as to its meaning and use.

```json
"options":
{
  ...
}
```

### xman
Specifies the name of an Xmanager.

```json
"xman": "PTXRUN20"
```
### abend_in
Indicates which module in the collection engine to force abends to occur.

Valid values are:

**For PDT:** DII or DIU

**For PSA:** coming soon

```json
"abend_in": "DII"
"abend_in": "DIU"
```

### wait_time_after_coll_init
Indicates in minutes how long to wait after a product collection has been started.  

```json
"wait_time_after_coll_init": 10
```

### wait_time_after_abend_restart
Indicates in minutes how long to wait after the abend restart functionality has completed before another forced abend restart is attempted.

```json
"wait_time_after_abend_restart": 60
```

### number_of_abend_restarts
Indicates how many times abend restart functionality should be driven in a single test.

```json
"number_of_abend_restarts": 4
```

### rtpj_file
The name of an RTPJ JSON file.

```json
"rtpj_file": "Select_Count_Test.JSON"
```

### rtpj_library
Indicates the library where the [rtpj_file](#rtpj_file) should be located.

```json
"rtpj_library": "C:\Users\spean03\Desktop\JSON\PDT1497"
```

### rtpj_sync
Indicates whether the calling of RTPJ to execute the [rtpj_file](#rtpj_file) is done as a synchronous or asynchronous process.

Valid values are **true** or **false**. Defaults to **true**

```json
"rtpj_sync": "true"
"rtpj_sync": "false"
```

### rtpj_log_level
Can be used to override the RTPJ frameworks **"LOG"** level used when executing the [rtpj_file](#rtpj_file). Defaults to **DEFAULT** which
indicates the behavior is based on value of the [rtpj_sync](#rtp_syn) parameter.

If **rtpj_sync** is set to **true** then the RTPJ default log level is used, which is **INFO**. If **rtpj_sync** is set to **false** then
the RTPJ log level is set to **ERROR**.

Valid values are the same as listed for the [LOG](/rtpj/running-tests.md#log)

```json
"rtpj_log_level": "ERROR"
"rtpj_log_level": "WARN"
```

### wait_to_complete
Use of the parameter can be different for each type of test. Refer to the documentation for the specific test as to its meaning and use.

```json
"wait_to_complete": "true"
"wait_to_complete": "False"
```

### text_type
Can be used to indicate dynamic or static SQL. Specific usage can be different for each type of test, refer to the documentation for the specific test.

```json
"text_type": "static"
"text_type": "dynamic"
```

### text list
A list composed of key/value pairs where the key is any string and the value an SQL text string.

```json
"text1": "SELECT * FROM SYSIBM.SYSDUMMY1"
```
