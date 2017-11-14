# Command Line Options
---
Options described below have a short and long version, prefixed with either `-` (*short option*) or `--` (*long option*) and can
override the parameters specified in the JSON input file and/or the frameworks default values.

See the specific [test documentation](creating-tests.md#test-structure) for the command line options that apply.

## lpar
The LPAR in which to connect to.

Example:

Short
```python
-lp=ca31
```
Long
```python
--lpar=ca31
```

## userid
The ID to use to log onto the LPAR.

Example:

Short
```python
-usr=spean03
```
Long
```python
--userid=speana3
```

## ssid
The primary SSID to be used for test execution.

Example:

Short
```python
-ss=d12a
```
Long
```python
--ssid=d12a
```

## ssid2
A second ssid to be used during test execution.

Example:

Short
```python
-ss2=d11a
```
Long
```python
--ssid2=d11a
```

## file
Specifies the name of the input file, in JSON format, that contains the test(s) to execute along with the parameters needed.
The `file` option can reference just a file name in which the indicated file will be searched for out of the default
test library, `/rtppy/python_test_library`. Or a complete path can be specified, which is useful to reference a JSON file located
on your local machine for individual executions, debugging, or future test development.

Example:

Short
```python
-f=view_by_tests.json
-f=C:\Users\spean03\Desktop\mytestparms.json
```
Long
```python
--file=view_by_tests.json
--file=C:\Users\spean03\Desktop\mytestparms.json
```

## print
The print option provides the functionality to print out to the console all the test descriptions (if coded in the JSON file) or the raw contents of the JSON file itself pointed to by the `--file` parameter. To print just the test descriptions just provide the option without a value. To print the raw contents provide the value "raw" with the option.

Examples:

**print just descriptions**
```python
-p --file=pdt_interval_compare_all_standard_activity_view_by_tests.json
```
**(print raw contents)**
```python
-p=raw --file=pdt_interval_compare_all_standard_activity_view_by_tests.json
```

## baseline_vcat
Overrides the VCAT name to be used to identify the baseline datastore to use.

Example:

Short
```python
-bv=PDTDBA.R19
```
Long
```python
--baseline_vcat=PDTDBA.R19
```

## baseline_datastore
Overrides the datastore that should be considered to contain the baseline execution metrics.

Example:

Short
```python
-bld=dtvnext
```
Long
```python
--baseline_datastore=dtvnext
```

## current_vcat
Overrides the VCAT name to be used to identify the current datastore to use.

Example:

Short
```python
-cv=PDTDBA.R19
```
Long
```python
--current_vcat=PDTDBA.R19
```

## current_datastore
Overrides the datastore that should be considered to contain the current execution metrics to compare against the baseline.

Example:

Short
```python
-cud=mycurrent
```
Long
```python
--current_datastore=mycurrent
```
## baseline_interval_date/current_interval_date
Overrides the interval date in the datastore that should be selected in combination with the corresponding interval time parameter.

#### Format
The interval date can be supplied as it appears on the products "Datastore Interval Summary Display" or a value string
of "1" can be used to indicate the most recent interval should be selected.

Using **16/05/13**:

##### Short
```python
-bld='16/05/13'
-cid='16/05/13'
```
**OR**
```python
-bid='1'
-cid='1'
```

##### Long
```python
--baseline_interval_date='16/05/13'
--current_interval_date='16/05/13'
```
**OR**
```python
--baseline_interval_date='1'
--current_interval_date='1'
```

## baseline_interval_time/current_interval_time
Further identifies and overrides the interval time in the datastore that should be selected in combination with the interval date parameter. Unless the interval date parameter indicates the most recent interval should be selected, in which the interval time parameter is ignored.

#### Format
The interval time should be supplied as it appears on the products "Datastore Interval Summary Display".

Using **02:00:00**:

##### Short
```python
-bit='02:00:00'
-cit='02:00:00'
```

##### Long
```python
--baseline_interval_time='02:00:00'
--current_interval_time='02:00:00'
```

## baseline_interval_date_2/current_interval_date_2
Overrides the second interval date in the datastore that should be selected in combination with the corresponding interval_time_2 parameter.

#### Format

##### Short
```python
-bld2='16/05/13'
-cid2='16/05/13'
```
**OR**

```python
-bid2='1'
-cid2='1'
```

##### Long
```python
--baseline_interval_date_2='16/05/13'
--current_interval_date_2='16/05/13'
```
**OR**

```python
--baseline_interval_date_2='1'
--current_interval_date_2='1'
```


## baseline_interval_time_2/current_interval_time_2
Overrides the second interval time in the datastore that should be selected in combination with the corresponding interval_date_2 parameter.

#### Format

##### Short
```python
-bit2='02:00:00'
-cit2='02:00:00'
```

##### Long
```python
--baseline_interval_time_2='02:00:00'
--current_interval_time_2='02:00:00'
```

## view_by
Override what Summary Display panel to navigate to.

Example:

Short
```python
-vb=S
```
Long
```python
--view_by=P
```

## view_type
Overrides what type of data displays to navigate to. (i.e. Standard Activity, Exceptions, Errors, etc...)

Example:

Short
```python
-vt=X
```
Long
```python
--view_type=E
```

## view_option
Override what additional Summary Display panel to navigate to within certain displays in Subsystem Analyzer

Example:

Short
```python
-vo=C
```
Long
```python
--view_option=C
```

## environment
Overrides the release environment of the products to use. This parameter overrides both the JSON input file and/or the frameworks
default of **R19**

Short
```python
-env=R19
```
Long
```python
--environment=R19
```
#### Entering via DB.ALL
To enter into the products using the "Extended General Selection Menu", i.e. DB.ALL using an overriding parmlib and/or suffix.
Simply specify the overriding parmlib and optional a suffix in **()**.

Example:
```python
--environment=SPEAN03.R19.PARMLIB(99)
```

## range_pct
Overrides the allowable plus or minus range percentage the comparison can be between. This parameter overrides the JSON parameter
specified and the tests default value.

Short
```python
-rp=15
```
Long
```python
--range_pct=15
```

## plan
Overrides the value that can be used to identify a row on a Planname Display or the keyword "ALL" which can indicate to some tests that all the Plans should be selected.

Short
```python
-pln=rtpplnmn
```

Long
```python
--plan=rtpplnmn
```

## program
Overrides the value that can be used to identify a row on a Program Display or the keyword "ALL" which can indicate to some tests that all the Programs should be selected.

Short
```python
-pgm=rtpplnmn
```

Long
```python
--program=rtpplnmn
```

## dbname
Overrides the value that can be used to identify a row on the Database Activity Display or the keyword "ALL" which indicates that all the Databases should be selected.

Short
```python
-db=SEGMDB
```

Long
```python
--dbname=SEGMDB
```

## key_option
Overrides the single character that is to be used in the "Key" field on the standard activity "Key Summary Display"

Short
```python
-ko=R
```
Long
```python
--key_option=R
```

## key_value
Overrides the value used to identify the row in the "Key" column on the standard activity Key Summary Display.

Short
```python
-kv='TSO BATCH'
```
Long
```python
--key_value='QARTP01'
```

## column
Overrides the specific column name used by a test. The use of the column name parameter can be different for each type of test.
Refer to the documentation for the specific test as to its meaning and use.

Long
```python
--column='INDB2_TIME'
```

## collid
Overrides the value used to identify a row on a display that contains the "COLLID" column

Long
```python
--collid='RTPCOLUMN'
```
## line_command
Overrides the single character line command option to be used on a display row.

Short
```python
-lc='D'
```

Long
```python
--line_command='D'
```

## wait_to_complete
Overrides the wait_to_complete parameter in the JSON file. Use of the parameter can be different for each type of test. Refer to the documentation for the specific test as to its meaning and use.

Short
```python
-wtc=False
```

Long
```python
--wait_to_complete=True
```

## xman
Overrides the Xmanager name.

Long
```python
--xman='PTXDEV19'
```

## abend_in
Overrides the value used in the JSON parameter for indicating which module in the collection engine to force abends to occur.

Valid values are:

**For PDT:** DII or DIU

**For PSA:** coming soon


Long
```python
--abend_in='DII'
```

## num_ar
Overrides the value used in the JSON parameter of how many times abend restart functionality should be driven in a single test.

Long
```python
--num_ar=3
```

## rtpj_file
Overrides the name of the RTPJ JSON to be used.

Long
```python
--rtpj_file=Select_Count_Test.JSON
```

## rtpj_library
Overrides the library location used in the JSON file.

Long
```python
--rtpj_library=C:\Users\spean03\Desktop\JSON\PDT1497
```

## rtpj_sync
Overrides the [rtpj_sync](json-parameters.md#rtpj_sync) parameter in the JSON file.

Long
```python
--rtpj_sync=true
```

## rtpj_log_level
Overrides the [rtpj_log_level](json-parameters.md#rtpj_log_level) parameter in the JSON file.

Long
```python
--rtpj_log_level=ERROR
```


## output_location
Overrides the specified directory location for the output of the test to be written to.

**Executing via Locally -** the directory can be any valid path on your local machine and the directory and file will be
 created for you automatically.

**Executing via Jenkins -** This parameter should not be altered.

Long
```python
--output_location=C:\Users\spean03\Desktop\output
```

## high_level
Overrides the high_level JSON parameter in the options object for starting a product collection.

Long
```python
--high_level=PDTDBA.R19
```

## collection_profile
Overrides the coll_profile JSON parameter in the options object for starting a Detector collection.

Long
```python
--collection_profile=COLLALL
```

## itime
Overrides the itime JSON parameter in the options object for starting a product collection.

Long
```python
--itime=24:00
```

## t_limit
Overrides the t_limit JSON parameter in the options object for starting a product collection.

Long
```python
--t_limit=01:00
```
## samp
Overrides the samp JSON parameter in the options object for starting a Subsystem Analyzer collection.

Long
```python
--samp=3
```