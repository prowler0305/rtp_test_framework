# RTP Test Suite App


The rtptest test type provides the ability to interact with the Real Time Performance Test Suite Application UI in order to 
generate the JCL and optionally submit it.

For more information about the RTP Test Suite capabilities and its parameters see the [RTP Test Suite manual](https://cawiki.ca.com/display/DB2QA/Real+Time+Performance+Testing+Tools).

### Jenkins Test Status
The table below lists the jenkins tests that are available and what the status of the last run of the test was. Click on
the status icon to go straight to jenkins for the particular build project.

Jenkins Build Name | Status
------------------ | ------

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
[execute_method](json-parameters.md#execute_method) | | The following additional JSON parameters are **required**, unless otherwise indicated, when **execute_method** is:<br> <ul><li>**UI**:</li><ul><li>**action** [[JSON]](json-parameters.md#action)</li></ul><li>**dataset**</li><ul><li>**dataset_name** [[JSON]](json-parameters.md#dataset_name)</li></ul></ul>

#### Optional
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[output_location](json-parameters.md#output_location) | [output_location](command-line-options.md#output_location)
[auto_submit](json-parameters.md#auto_submit) | 
[multithreading](json-parameters.md#multithreading) | 
[multiple_plan_packages](json-parameters.md#multiple_plan_packages) | 
[wait_to_complete](json-parameters.md#wait_to_complete) |  [wait_to_complete](command-line-options.md#wait_to_complete) | Indicates whether the test should wait for the submitted RTPTEST batch job to complete or not. Valid values are **True** or **False**
[options](json-parameters.md#options) | | Identifies additional options to be used. See the [Additional Options](#additional-options) section for details.

#### Additional Options

JSON parameter | Special Usage or Note
-------------- | ---------------------
program | Can specify either a single program or a list of programs separated by commas.<br> Example: PROGRAM1,PROGRAM2,PROGRAM3
plan | 
collid | 
corrid |
sqlid |
workstation |
repeat |
seed| 

# JSON Examples
---

#### Create Objects
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "2"
    }
  ]
}
```

#### Compile Program (a RRSAF program)
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "3",
      "options": 
      {
        "program": "reg161br",
        "connection_type": "R"
      }
    }
  ]
}
```
#### Bind All Programs with Multi Plan/Packages
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "4",
      "multiple_plan_packages": "Y"
    }
  ]
}
```
#### Bind Single Program (changing collection id from the default and including the plan binding)
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "5",
      "include_plan": "Y",
      "options": 
      {
       "collid": "mycollidisbigger",
       "program": "reg152dr"
      }
    }
  ]
}
```
#### Execute All Programs (via Multi Threading)
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "6",
      "multithreading": "Y"
    }
  ]
}
```
#### Execute All Programs (via Multiple Plan/Packages)
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "6",
      "multiple_plan_packages": "Y"
    }
  ]
}
```
#### Execute Program(s) (a single RRSAF Program with other parameters defaults)
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "7",
      "options": 
      {
        "connection_type": "R",
        "program": "reg021sr"
      }
    }
  ]
}
```
#### Execute Program(s) (a list of RRSAF Program with other parameters defaults)
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "7",
      "options": 
      {
        "connection_type": "R",
        "program": "reg161br,reg011dr,reg165br,reg133dr"
      }
    }
  ]
}
```
#### Execute Program(s) (an RRSAF Program with changing other parameters)
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "7",
      "options": 
      {
        "program": "reg161br",
        "collid": "mycollidisbigger",
        "corrid": "mycorridisbigger",
        "workstation": "myworkstation",
        "repeat": "10",
        "sqlid": "mysqlid",
        "plan": "myplan",
        "seed": "5"
      }
    }
  ]
}
```
#### Free All PKGE/PLAN with Multi Plan/Packages
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "8",
      "multiple_plan_packages": "Y"
    }
  ]
}
```
#### Free Single Program
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "9",
      "options": 
      {
       "program": "reg165br"
      }
    }
  ]
}
```
#### Cleanup
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
    "ssid2": "d11a"
  },
  "tests":
  [
    {
      "test_type": "rtptest",
      "product_code": "RTP",
      "execute_method": "UI",
      "action": "10"
    }
  ]
}
```