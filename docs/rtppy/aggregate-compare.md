# Aggregate Compare


The Aggregate Compare test type can aggregate a display of lower data and compare it to a higher display of data.
(i.e. aggregate the statement data and compare it to the program data)

### Jenkins Test Status
The table below lists the jenkins tests that are available and what the status of the last run of the test was. Click on
the status icon to go straight to jenkins for the particular build project.

Jenkins Build Name | Status
------------------ | ------
PDT_aggregate_compare_all_standard_activity | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_all_standard_activity/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_all_standard_activity/)
PDT_aggregate_oompare_plan_level_single_test | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_plan_level_single_test/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_plan_level_single_test/)
PDT_aggregate_oompare_program_level_single_test | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_program_level_single/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_program_level_single/)
PDT_aggregate_oompare_key_level_single_test | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_key_level_single/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Aggregate%20Compare%20Tests/job/PDT_aggregate_compare_key_level_single/)
PSA_aggregate_oompare_dbase_level_single_test | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PSA/job/PSA_aggregate_compare_dbase_level_single/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PSA/job/PSA_aggregate_compare_dbase_level_single/)

## Test Parameters
The table below lists the required and optional parameters that are valid for this test. Follow the link by clicking on the
parameter name in the JSON column. If the parameter has a command line override option it will be listed in the Command Line Override
column. Additionally there are [examples](#json-examples) at the bottom of this page.

#### Required
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[product_code](json-parameters.md#product_code) |
[test_type](json-parameters.md#test_type) |
[lpar](json-parameters.md#lpar) | [lpar](command-line-options.md#lpar)
[userid](json-parameters.md#userid) | [userid](command-line-options.md#userid)
[ssid](json-parameters.md#ssid) | [ssid](command-line-options.md#ssid)
[current_vcat](json-parameters.md#current_vcat) | [current_vcat](command-line-options.md#current_vcat)
[current_datastore](json-parameters.md#current_datastore) | [current_datastore](command-line-options.md#current_datastore)
[current_interval_date](json-parameters.md#baseline_interval_datecurrent_interval_date) | [current_interval_date](command-line-options.md#baseline_interval_datecurrent_interval_date)
[current_interval_time](json-parameters.md#baseline_interval_timecurrent_interval_time) | [current_interval_time](command-line-options.md#baseline_interval_timecurrent_interval_time)
[level](json-parameters.md#level) | | The following additional JSON parameters are **required**, unless otherwise indicated, when **level** is:<br> <ul><li>**PLAN**:</li><ul><li>**plan** [[JSON]](json-parameters.md#plan) [[command line]](command-line-options.md#plan)</li></ul><li>**PROGRAM**</li><ul><li>**plan**</li><li>**program** [[JSON]](json-parameters.md#program) [[command line]](command-line-options.md#program)</li><ul><li>**collid** [[JSON]](json-parameters.md#collid) [[command line]](command-line-options.md#collid) - **required** if **program** parameter indicates a specific program name.</li></ul><li>**KEYS**</li><ul><li>**key_value** [[JSON]](json-parameters.md#key_value) [[command line]](command-line-options.md#key_value)</li><li>**line_command**(optional) [[JSON]](json-parameters.md#line_command) [[command line]](command-line-options.md#line_command) - Valid values are **P** or **G** - Defaults to **P**.<ul><li>Used to indicate if aggregating Plan data or Program data to the Key Summary display for the **key_value** indicated.</li></ul></li><li>**key_option**(optional) [[JSON]](json-parameters.md#key_option) [[command line]](command-line-options.md#key_option) - Defaults to **"U"**.</li></ul></ul><li>**DBASE**:</li><ul><li>**dbname** [[JSON]](json-parameters.md#dbname) [[command line]](command-line-options.md#dbname)</li></ul></ul>

#### Optional
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[environment](json-parameters.md#environment) | [environment](command-line-options.md#environment)
[output_location](json-parameters.md#output_location) | [output_location](command-line-options.md#output_location)
[column](json-parameters.md#column) | [column](command-line-options.md#column) | Can be used to indicate that only the data in the specified column should be compared for the test.
[current_interval_date_2](json-parameters.md#baseline_interval_date_2current_interval_date_2) | [current_interval_date_2](command-line-options.md#baseline_interval_date_2current_interval_date_2)
[current_interval_time_2](json-parameters.md#baseline_interval_time_2current_interval_time_2) | [current_interval_time_2](command-line-options.md#baseline_interval_time_2current_interval_time_2)

# JSON Examples
---

#### Aggregate program stats to plan level for all plans

```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "PLAN",
	    "plan": "ALL"
      }
    ]
}
```
#### Aggregate program stats to plan level for a specific plan only.

```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "PLAN",
	    "plan": "RTPPLNMN"
      }
    ]
}
```
#### Aggregate statement stats to program level for all programs in a plan.

```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "PROGRAM",
	    "plan": "RTPPLNMN",
        "program": "ALL"
      }
    ]
}
```
#### Aggregate statement stats to program level for a specific program.
```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "PROGRAM",
	    "plan": "RTPPLNMN",
        "program": "REG133DR",
        "collid": "RTPCOLMN"
      }
    ]
}
```
#### Aggregate plan stats to key level for a ALL keys.
```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "KEYS",
	    "key_value": "ALL"
      }
    ]
}
```
#### Aggregate plan stats to key level for a specific key.
```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "KEYS",
	    "key_option": "U",
	    "key_value": "SPEAN03",
	    "line_command": "P"
      }
    ]
}
```

#### Aggregate program stats to key level for ALL keys.
```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "KEYS",
	    "key_option": "U",
	    "key_value": "ALL",
	    "line_command": "G"
      }
    ]
}
```

#### Aggregate program stats to key level for particular key.
```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "level": "KEYS",
	    "key_option": "C",
	    "key_value": "TSO CAF",
	    "line_command": "G"
      }
    ]
}
```
#### Aggregate program stats to plan level for all plans for a range of intervals

```json
{
    "connection":
    {
      "lpar": "ca31",
      "ssid": "d12a",
      "userid": "QARTP01"
    },
    "tests":
    [
      {
        "test_type": "aggregate compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "python",
        "current_interval_date": "16/07/20",
        "current_interval_date_2": "16/07/20",
        "current_interval_time": "10:42:34",
        "current_interval_time_2": "12:42:34",
        "level": "PLAN",
	    "plan": "ALL"
      }
    ]
}
```
