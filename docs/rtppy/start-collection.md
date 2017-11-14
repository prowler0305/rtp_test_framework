# Start/Stop Collection

This test type can start or stop a product collection.

### Jenkins Test Status
The table below lists the jenkins tests that are available and what the status of the last run of the test was. Click on
the status icon to go straight to jenkins for the particular build project.

Jenkins Build Name | Status
------------------ | ------
RTPPY_start_collection | [![Build Status](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/RTPPY_start_collection/badge/icon)](http://plape03-u114063:8080/job/DB2%20Tools/job/RTP/job/RTPPY/job/RTPPY_start_collection/?style=plastic)

## Test Parameters
The table below lists the required and optional parameters that are valid for this test. Follow the link by clicking on the
parameter name in the JSON column. If the parameter has a command line override option it will be listed in the Command Line Override
column. Additionally there are [examples](#json-examples) at the bottom of this page.

#### Required
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[product_code](json-parameters.md#product_code) |
[test_type](json-parameters.md#test_type) | | For starting a collection specify "start collection", to stop specify "stop collection"
[lpar](json-parameters.md#lpar) | [lpar](command-line-options.md#lpar)
[userid](json-parameters.md#userid) | [userid](command-line-options.md#userid)
[ssid](json-parameters.md#ssid) | [ssid](command-line-options.md#ssid)
[options](json-parameters.md#options) | | Identifies the collection options to be used. See the [Collection Options](#collection-options) section for details on each products collection option and how to specify it.

#### Collection Options
The following tables below lists the product collection option and its corresponding JSON parameter name specified in the **options** parameter in the JSON file.

[Parameters used by both products](#common-collection-options)

[Detector](#detector-collection-options)

[Subsystem Analyzer](#subsystem-analyzer-collection-options)

---

##### Common Collection Options
Collection Option Name | JSON parameter | Default if not specified | Command Line Override | Special Usage or Note
- | - | - | - | -
DB2 SSID | ssid | SSID specified in the connection information of the JSON file | | **(Optional)** - If present, indicates the collection should be started for an SSID other than the SSID specified in the JSON connection information section.
Interval Time | itime | 01:00 (1 hour) | [Yes](command-line-options.md#itime)
Round Interval | r_interval | N |
Use Sysplex Interval Time | plex_time | N |
Time Limit | t_limit | 00:00 (no limit) | [Yes](command-line-options.md#t_limit)
Externalize | extern | N |
High Level | high_level | | [Yes](command-line-options.md#high_level) | **Required**
Datastore Name | current_datastore | | [Yes](command-line-options.md#current_datastore) | **Required**
Auto Start | auto | N |

##### Detector Collection Options
Collection Option Name | JSON parameter | Default if not specified | Command Line Override |Special Usage or Note
- | - | - | - |-
Triggered SQL | trig_sql | N |
Plan Excl/Incl List | exclude_list | N |
Standard Activity | standard | N |
Dynamic SQL Stats | dynam_stats | N |
View By Keys | view_keys | N |
Dynamic Exceptions | dynam_excp | N |
Static Exceptions | static_excp | N |
SQL Errors | sql_errors | N |
SQL Error Text | error_text | N |
Host Variables | host_vars | N |
Collection Profile | coll_profile | *blanks* | [Yes](command-line-options.md#collection_profile) | **Required**
Exception cache size MB | excp_cache | 0000 |

##### Subsystem Analyzer Collection Options
Collection Option Name | JSON parameter | Default if not specified | Command Line Override | Special Usage or Note
- | - | - | - | -
Volume and Extent | vol_ext | Y |
Sampling Rate | samp | 100 | [Yes](command-line-options.md#samp) |

# JSON Examples
---

#### Start a Detector Collection
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp01",
    "ssid": "d12a"
  },
  "tests":
  [
    {
      "test_type": "start collection",
      "product_code": "PDT",
      "environment": "PDTDBA.RTPQA.PARMLIB",
      "options":
      {
        "itime": "00:15",
        "t_limit": "00:99",
        "extern": "Y",
        "high_level": "PDTDBA.python",
        "data_store": "TSTSTART",
        "coll_profile": "DEFAULT",
        "trig_sql": "Y",
        "exclude_list": "Y",
        "standard": "Y",
        "dynam_stats": "Y",
        "view_keys": "Y",
        "dynam_excp": "Y",
        "static_excp": "Y",
        "sql_errors": "Y",
        "error_text": "Y",
        "host_vars": "Y",
        "excp_cache": "0020"
      }
    }
  ]
}
```

#### Start a Subsystem Analyzer Collection
```json
{
  "connection":
  {
    "lpar": "ca31",
    "userid": "qartp01",
    "ssid": "d12a"
  },
  "tests":
    [
      {
        "test_type": "start collection",
        "product_code": "PSA",
        "environment": "PDTDBA.RTPQA.PARMLIB",
        "options":
        {
          "itime": "00:15",
  	      "t_limit": "00:99",
  	      "extern": "Y",
  	      "high_level": "PDTDBA.R19",
  	      "data_store": "RTPCURNT",
  	      "vol_ext": "N",
  	      "samp": "6"
        }
      }
    ]
}
```
