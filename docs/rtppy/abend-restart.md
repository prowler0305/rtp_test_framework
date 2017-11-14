# Abend Restart


This test type can drive the PDT and PSA abend restart feature by setting abends to occur in different areas of the products
collection engine. Then uses the RTPJ framework to submit just the right amount of activity to cause enough abends to get the
collections to terminate allowing abend restart to be invoked naturally.

Because of the nature of this test altering code in collection engine modules that is directly execute by threads in the DB2
address space and modules that remain loaded for the duration of the xmanager address space. It is highly suggested that users
understand the implications of running this test on DB2 SSID's and XMANAGERS that are used by the entire development
community (i.e. xmanagers that service the PRD, DEV, QA, and CURIR environments).

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
[xman](json-parameters.md#xman) | [xman](command-line-options.md#xman)
[abend_in](json-parameters.md#abend_in) | [abend_in](command-line-options.md#abend_in)

#### Optional
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[output_location](json-parameters.md#output_location) | [output_location](command-line-options.md#output_location)
[wait_time_after_coll_init](json-parameters.md#wait_time_after_coll_init) | | Defaults to 6 minutes if not specified. More info on how to use the wait times in section [How to use wait times](#how-to-use-wait-times)
[wait_time_after_abend_restart](json-parameters.md#wait_time_after_abend_restart) | | Defaults to 61 minutes if not specified. More info on how to use the wait times in section [How to use wait times](#how-to-use-wait-times)
[number_of_abend_restarts](json-parameters.md#number_of_abend_restarts) | [num_ar](command-line-options.md#num_ar) | Defaults to 2.
[options](json-parameters.md#options) | | Identifies the options to be used to start a product collection as defined in the [Collection Options](start-collection.md#collection-options) section of the Start Collections test type.


#### How to use wait times
The wait time parameters are used correlate with the design of the abend restart feature. The time limits within the abend restart feature can be exercised by using the number_of_abend_restarts combined with the single or combined use of the wait_time_after_coll_init and wait_time_after_abend_restart parameters. See some of the JSON examples below.  

# JSON Examples
---

#### Execute Abend Restart in PDT forcing an abend in DII 6 minutes after the first collection start and 60 minutes after the abend restart.
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
          "test_type": "abend restart",
          "product_code": "PDT",
    	  "environment": "SPEAN03.R19.PARMLIB(IR)",
    	  "xman": "PTX0005",
    	  "abend_in": "DII",
    	  "options":
          {
    		"itime": "00:05",
            "t_limit": "00:00",
            "extern": "N",
            "collection_profile": "COLLALL",
    		"standard": "Y"
          }
    }
  ]
}
```

#### No abend restart within 5 minutes of initial starting of collection
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp02",
    "ssid": "d11a",
  },
  "tests":
  [
    {
          "test_type": "abend restart",
          "product_code": "PDT",
    	  "environment": "SPEAN03.R19.PARMLIB(IR)",
    	  "xman": "PTX0005",
    	  "abend_in": "DII",
    	  "number_of_abend_restarts": 1,
    	  "wait_time_after_coll_init": 3,
    	  "options":
          {
    		"itime": "00:05",
            "t_limit": "00:00",
            "extern": "N",
            "collection_profile": "COLLALL",
    		"standard": "Y"
          }
    }
  ]
}
```

#### Execute Abend Restart in PDT forcing an abend in DIU 6 minutes after the first collection start but within 60 minutes after the abend restart.
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
          "test_type": "abend restart",
          "product_code": "PDT",
    	  "environment": "SPEAN03.R19.PARMLIB(IR)",
    	  "xman": "PTX0005",
    	  "abend_in": "DIU",
    	  "wait_time_after_abend_restart": 10,
    	  "wait_time_after_coll_init": 6,
    	  "options":
          {
    		"itime": "00:05",
            "t_limit": "00:00",
            "extern": "N",
            "collection_profile": "COLLALL",
    		"standard": "Y"
          }
    }
  ]
}
```

#### Execute Abend Restart in PDT forcing an abend in DIU 6 minutes after the first collection start and 60 minutes after the abend restart twice.
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
          "test_type": "abend restart",
          "product_code": "PDT",
    	  "environment": "SPEAN03.R19.PARMLIB(IR)",
    	  "xman": "PTX0005",
    	  "abend_in": "DII",
    	  "number_of_abend_restarts": 3,
    	  "options":
          {
    		"itime": "00:05",
            "t_limit": "00:00",
            "extern": "N",
            "collection_profile": "COLLALL",
    		"standard": "Y"
          }
    }
  ]
}
```

