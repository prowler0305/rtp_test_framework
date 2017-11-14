# Distributed SQL


The Distributed SQL test type gives the ability to execute distributed SQL via RTPJ from python. This can be useful when
driving SQL activity during a RTPPY automation test is needed.


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
[rtpj_file](json-parameters.md#rtpj_file) | [rtpj_file](command-line-options.md#rtpj_file)

#### Optional
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[environment](json-parameters.md#environment) | [environment](command-line-options.md#environment)
[output_location](json-parameters.md#output_location) | [output_location](command-line-options.md#output_location)
[rtpj_library](json-parameters.md#rtpj_library) | [rtpj_library](command-line-options.md#rtpj_library)
[rtpj_sync](json-parameters.md#rtpj_sync) | [rtpj_sync](command-line-options.md#rtpj_sync)
[rtpj_log_level](json-parameters.md#rtpj_log_level) | [rtpj_log_level](command-line-options.md#rtpj_log_level)

# JSON Examples
---

#### Execute distributed SQL via RTPJ from the internal test library

```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp03",
    "ssid": "d11a"
  },
  "tests":
  [
    {
      "test_type": "distributed sql",
      "product_code": "PDT",
      "rtpj_file": "Select_Count_Test.JSON",
      "rtpj_library": ""
    }
  ]
}
```
#### Execute distributed SQL via RTPJ from a local library.

```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp03",
    "ssid": "d11a"
  },
  "tests":
  [
    {
      "test_type": "distributed sql",
      "product_code": "PDT",
      "rtpj_file": "Select_Count_Test.JSON",
      "rtpj_library": "C:\Users\spean03\Desktop\JSON\PDT1497"
    }
  ]
}
```
