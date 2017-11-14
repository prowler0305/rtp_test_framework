# Interval Compare


The Interval Compare test type can validate all the data for an interval by comparing all the data at a summary display level, i.e.
Plan Summary, Program Summary, Statement Summary etc, between a baseline and a current set of data.

### Jenkins Test Status
The table below lists the jenkins tests that are available and what the status of the last run of the test was. Click on
the status icon to go straight to jenkins for the particular build project.

Jenkins Build Name | Status
------------------ | ------
PDT_all_standard_activity_Interval_compare_summary_levels | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Interval%20Compare%20Tests/job/PDT_all_standard_activity_Interval_compare_summary_levels/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Interval%20Compare%20Tests/job/PDT_all_standard_activity_Interval_compare_summary_levels/)
PDT_interval_compare_single_view_by_test | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Interval%20Compare%20Tests/job/PDT_interval_compare_single_view_by_test/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PDT%20Interval%20Compare%20Tests/job/PDT_interval_compare_single_view_by_test/)
PSA_all_object_activity_interval_compare_summary_levels | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PSA/job/PSA_all_object_activity_interval_compare_summary_levels/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PSA/job/PSA_all_object_activity_interval_compare_summary_levels/)
PSA_interval_compare_single_view_by_test | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PSA/job/PSA_interval_compare_single_view_by_test/badge/icon?style=plastic)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/PSA/job/PSA_interval_compare_single_view_by_test/)

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
[baseline_vcat](json-parameters.md#baseline_vcat) | [baseline_vcat](command-line-options.md#baseline_vcat)
[baseline_datastore](json-parameters.md#baseline_datastore) | [baseline_datastore](command-line-options.md#baseline_datastore)
[baseline_interval_date](json-parameters.md#baseline_interval_datecurrent_interval_date) | [baseline_interval_date](command-line-options.md#baseline_interval_datecurrent_interval_date)
[baseline_interval_time](json-parameters.md#baseline_interval_timecurrent_interval_time) | [baseline_interval_time](command-line-options.md#baseline_interval_timecurrent_interval_time)
[current_vcat](json-parameters.md#current_vcat) | [current_vcat](command-line-options.md#current_vcat)
[current_datastore](json-parameters.md#current_datastore) | [current_datastore](command-line-options.md#current_datastore)
[current_interval_date](json-parameters.md#baseline_interval_datecurrent_interval_date) | [current_interval_date](command-line-options.md#baseline_interval_datecurrent_interval_date)
[current_interval_time](json-parameters.md#baseline_interval_timecurrent_interval_time) | [current_interval_time](command-line-options.md#baseline_interval_timecurrent_interval_time)
[view_by](json-parameters.md#view_by) | [view_by](command-line-options.md#view_by)

#### Optional
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[environment](json-parameters.md#environment) | [environment](command-line-options.md#environment)
[output_location](json-parameters.md#output_location) | [output_location](command-line-options.md#output_location)
[range_pct](json-parameters.md#range_pct) | [range_pct](command-line-options.md#range_pct) | Default - 10% if not specified.
[view_type](json-parameters.md#view_type) | [view_type](command-line-options.md#view_type) | If not provided then products default is used.
[view_option](json-parameters.md#view_option) | [view_option](command-line-options.md#view_option) | Applies only to Subsystem Analyzer.
[key_option](json-parameters.md#key_option) | [key_option](command-line-options.md#key_options) | If **view_by=K** must be specified otherwise error occurs.
[ssid2](json-parameters.md#ssid2) | [ssid2](command-line-options.md#ssid2) | If provided indicates the baseline_datastore is for a different ssid than the primary.
[column](json-parameters.md#column) | [column](command-line-options.md#column) | Can be used to indicate that only the data in the specified column should be compared for the test.
[baseline_interval_date_2](json-parameters.md#baseline_interval_date_2current_interval_date_2) | [baseline_interval_date_2](command-line-options.md#baseline_interval_date_2current_interval_date_2)
[baseline_interval_time_2](json-parameters.md#baseline_interval_time_2current_interval_time_2) | [baseline_interval_time_2](command-line-options.md#baseline_interval_time_2current_interval_time_2)
[current_interval_date_2](json-parameters.md#baseline_interval_date_2current_interval_date_2) | [current_interval_date_2](command-line-options.md#baseline_interval_date_2current_interval_date_2)
[current_interval_time_2](json-parameters.md#baseline_interval_time_2current_interval_time_2) | [current_interval_time_2](command-line-options.md#baseline_interval_time_2current_interval_time_2)


# JSON Examples
---

#### Non-Key Display Example
```json
{
    "connection":
    {
      "lpar": "ca31",
      "userid": "qartp01",
      "ssid": "d12a",
      "ssid2": "d11a"
    },
 "tests":
    [
      {
        "test_type": "interval compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "baseline_vcat": "PDTDBA.SPEAN03",
        "baseline_datastore": "PYTHON",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "PYTHON",
        "baseline_interval_date": "16/07/20",
        "baseline_interval_time": "10:07:09",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "view_by": "S",
        "view_type": "A"
      }
    ]
}
```

#### Key Display Example
```json
{
    "connection":
    {
      "lpar": "ca31",
      "userid": "qartp01",
      "ssid": "d12a",
      "ssid2": "d11a"
    },
 "tests":
    [
      {
        "test_type": "interval compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "baseline_vcat": "PDTDBA.SPEAN03",
        "baseline_datastore": "PYTHON",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "PYTHON",
        "baseline_interval_date": "16/07/20",
        "baseline_interval_time": "10:07:09",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "view_by": "K",
        "key_option": "R",
        "view_type": "A",
        "range_pct": 15
      }
    ]
}
```
#### Compare only a specific column of data
```json
{
    "connection":
    {
      "lpar": "ca31",
      "userid": "qartp01",
      "ssid": "d12a",
      "ssid2": "d11a"
    },
 "tests":
    [
      {
        "test_type": "interval compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "baseline_vcat": "PDTDBA.SPEAN03",
        "baseline_datastore": "PYTHON",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "PYTHON",
        "baseline_interval_date": "16/07/20",
        "baseline_interval_time": "10:07:09",
        "current_interval_date": "16/07/20",
        "current_interval_time": "10:42:34",
        "view_by": "G",
        "view_type": "A",
        "column": "INDB2_TIME"
      }
    ]
}
```
#### Selecting a range of intervals
```json
{
    "connection":
    {
      "lpar": "ca31",
      "userid": "qartp01",
      "ssid": "d12a",
      "ssid2": "d11a"
    },
 "tests":
    [
      {
        "test_type": "interval compare",
        "product_code": "PDT",
        "environment": "SPEAN03.R19.PARMLIB",
        "baseline_vcat": "PDTDBA.SPEAN03",
        "baseline_datastore": "PYTHON",
        "current_vcat": "PDTDBA.SPEAN03",
        "current_datastore": "PYTHON",
        "baseline_interval_date": "16/07/20",
        "baseline_interval_time": "10:07:09",
        "baseline_interval_date_2": "16/07/20",
        "baseline_interval_time_2": "12:07:09",
        "current_interval_date": "16/07/20",
        "current_interval_time": "12:42:34",
        "current_interval_date_2": "16/07/20",
        "current_interval_time_2": "12:42:34",
        "view_by": "S",
        "view_type": "A"
      }
    ]
}
```
