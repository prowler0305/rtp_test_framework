# SQL Text

This test type provides different ways of testing the SQL Text obtained by Detector depending on the supplied parameters.
See the list below for the different sub-tests.

##### Test 1:
Was SQL text obtained for the statements executed under a given program under a plan.

* This is the test that is always performed which minimum validates that the SQL Text display for the SQL statement is accessible without an error indicating the SQL text could not be located. The text is then extracted from this display and put in the report that is generated at the end of the test. This gives a quick overall visual for each program under the plan what the statement was and the SQL Text that appears when selecting that statement. See an example of the output [here](#example-output-for-test-1).
 
##### Test 2:
Does the SQL text collected equally compare to the source SQL that was executed. 

* This level of validation testing is only done when the optional parameter [text list](#anchorlist) is included in the test, see the [example](#jsonwithtextlist) of how to use the parameter. When present the SQL text obtained in [test 1](#test-1) is searched against the specified list for a match. An additional column is added to the same report produced by test 1 that is either left blank or contains the text from the list that matched the display text. An additional report is included for any SQL text from the user provided text list that no match was found. See an example of the output [here](#example-output-for-test-2).     

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
[plan](json-parameters.md#plan) | [plan](command-line-options.md#plan)
[program](json-parameters.md#program) | [program](command-line-options.md#program) | Provide a specific program name or value of **ALL** to indicate all programs under the requested plan should be tested.
[collid](json-parameters.md#collid) | [collid](command-line-options.md#collid)|Required only if **program** parameter indicates a specific name.

#### Optional <a name="anchorlist"></a>
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[environment](json-parameters.md#environment) | [environment](command-line-options.md#environment)
[output_location](json-parameters.md#output_location) | [output_location](command-line-options.md#output_location)
[current_interval_date_2](json-parameters.md#baseline_interval_date_2current_interval_date_2) | [current_interval_date_2](command-line-options.md#baseline_interval_date_2current_interval_date_2)
[current_interval_time_2](json-parameters.md#baseline_interval_time_2current_interval_time_2) | [current_interval_time_2](command-line-options.md#baseline_interval_time_2current_interval_time_2)
[text_type](json-parameters.md#text_type) | |Indicates if the SQL executed under the program(s) is dynamic or static. Defaults to static.
[text list](json-parameters.md#text-list) | |The list of SQL text to compare against the text obtained from the product displays. The list is composed of key/value pairs where the key is any string and the value is the correct version of the SQL text that would have been executed. 

# JSON Examples
---

#### Access the static SQL for a specific plan and program

```json
{
  "connection": {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11b"
  },
  "tests": [
    {
      "test_type": "sql text",
      "environment": "SPEAN03.R20.PARMLIB(99)",
      "product_code": "PDT",
      "current_vcat": "PDTDBA.R19",
      "current_datastore": "PDT1511",
      "current_interval_date": "1",
      "current_interval_time": "20:37:26",
      "plan": "RCUUD190",
      "program": "PTASSPI",
      "collid": "AUTHD190_BSSP"
    }
  ]
}
```

#### Access the dynamic SQL for all the programs for a specific plan

```json
{
  "connection": {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11b"
  },
  "tests": [
    {
      "test_type": "sql text",
      "environment": "SPEAN03.R20.PARMLIB(99)",
      "product_code": "PDT",
      "current_vcat": "PDTDBA.R19",
      "current_datastore": "PDT1511",
      "current_interval_date": "1",
      "current_interval_time": "20:37:26",
      "plan": "DISTSERV",
      "program": "ALL",
      "text_type": "dynamic"
    }
  ]
}
```

#### Access the dynamic SQL for all the programs for a specific plan and validate it against a list of user specified SQL Text. <a name="jsonwithtextlist"></a>

```json
{
  "connection": {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11b"
  },
  "tests": [
    {
      "test_type": "sql text",
      "environment": "SPEAN03.R20.PARMLIB(99)",
      "product_code": "PDT",
      "current_vcat": "PDTDBA.R19",
      "current_datastore": "PDT1511",
      "current_interval_date": "1",
      "current_interval_time": "20:37:26",
      "plan": "DISTSERV",
      "program": "ALL",
      "text_type": "dynamic",
      "text list":
            {
              "text1": "SELECT  COUNT ( * ) FROM SYSIBM.SYSPACKAGE",
              "text2": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'T'",
              "text3": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'V'",
              "text4": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'A'",
              "text5": "SELECT  COUNT ( DISTINCT CREATOR ) FROM SYSIBM.SYSTABLES",
              "text6": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLESPACE",
              "text7": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'M'",
              "text8": "SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'F'",
              "text9": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSTRIGGERS' AND TBCREATOR = 'SYSIBM'",
              "text10": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSVIEWS' AND TBCREATOR = 'SYSIBM'",
              "text11": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'CREATESTMT' AND TBNAME = 'SYSROUTINES_SRC' AND TBCREATOR = 'SYSIBM'",
              "text12": "SELECT  COUNT ( * ) FROM SYSIBM.SYSINDEXES",
              "text13": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABCONST",
              "text14": "SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'P'",
              "text15": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'STMT' AND TBNAME = 'SYSPACKSTMT' AND TBCREATOR = 'SYSIBM'",
              "text16": "SELECT  COUNT ( * ) FROM SYSIBM.SYSSYNONYMS",
              "text17": "SELECT  COUNT ( * ) FROM SYSIBM.SYSDATATYPES WHERE OWNERTYPE = ''",
              "text18": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTRIGGERS",
              "text19": "SELECT  COUNT ( * ) FROM SYSIBM.SYSSEQUENCES",
              "text20": "SELECT  COUNT ( * ) FROM SYSIBM.XSROBJECTS"
            }
    }
  ]
}
```

# Example Output

#### Example Output for Test 1

##### Example 1:
Test output when specifying the minimum type of test parameters. Where the SQL Text for all the statements executed under the program specified were extracted successfully.

###### JSON file input
```json
{
  "connection": {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11b"
  },
  "tests": 
  [
    {
      "test_type": "sql text",
      "environment": "R20",
      "product_code": "PDT",
      "current_vcat": "PDTDBA.R19",
      "current_datastore": "QATEST19",
      "current_interval_date": "1",
      "current_interval_time": "20:37:26",
      "plan": "RCUUD190",
      "program": "PTASSPI",
      "collid": "AUTHD190_BSSP"
    }
  ]
}
```

###### Report Output

<div style="overflow-x:hidden;overflow-y:hidden;width:355%">

    <pre>-----------------------------------------------------------------------------------</br>
    2017-08-21                               SQL Text Captured Report          12:01:36
    
    2017-08-21-12:01:36, PLAN:  RCUUD190
    
    2017-08-21-12:01:36, PROGRAM:  PTASSPI 
    
    2017-08-21-12:01:36, SQL_CALL STMT#    SECT#    TEXT CAPTURED BY PRODUCT
    2017-08-21-12:01:36, -------- -------- -------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    2017-08-21-12:01:36, CONNT2   0000948  00000    CONNECT                                                                                                                                                                                                                                                                                                                                                                 
    2017-08-21-12:01:36, FETCH    0001046  00001    DECLARE CURSOR2 CURSOR FOR SELECT  A.SQL_TEXT_CREATOR , A.SQL_TEXT_NAME , A.SQL_SHARE , A.SQL_PANEL , A.SQL_DESCRIPTION , A.SQL_WHERE_TEXT , A.SQL_ORDER_TEXT , A.SQL_TABLE_NAME , A.SQL_TABLE_CREATOR , A.SQL_DEFAULT , A.SQL_QUERY_TYPE FROM PTI.PTSQL_TEXT_115 A WHERE A.SQL_TEXT_CREATOR = :H AND A.SQL_PRODUCT = :H AND A.SQL_PANEL LIKE :H AND A.SQL_DEFAULT = 'Y'
    2017-08-21-12:01:36, OPEN     0001039  00001    DECLARE CURSOR2 CURSOR FOR SELECT  A.SQL_TEXT_CREATOR , A.SQL_TEXT_NAME , A.SQL_SHARE , A.SQL_PANEL , A.SQL_DESCRIPTION , A.SQL_WHERE_TEXT , A.SQL_ORDER_TEXT , A.SQL_TABLE_NAME , A.SQL_TABLE_CREATOR , A.SQL_DEFAULT , A.SQL_QUERY_TYPE FROM PTI.PTSQL_TEXT_115 A WHERE A.SQL_TEXT_CREATOR = :H AND A.SQL_PRODUCT = :H AND A.SQL_PANEL LIKE :H AND A.SQL_DEFAULT = 'Y'
    2017-08-21-12:01:36, CLOSE    0001085  00001    DECLARE CURSOR2 CURSOR FOR SELECT  A.SQL_TEXT_CREATOR , A.SQL_TEXT_NAME , A.SQL_SHARE , A.SQL_PANEL , A.SQL_DESCRIPTION , A.SQL_WHERE_TEXT , A.SQL_ORDER_TEXT , A.SQL_TABLE_NAME , A.SQL_TABLE_CREATOR , A.SQL_DEFAULT , A.SQL_QUERY_TYPE FROM PTI.PTSQL_TEXT_115 A WHERE A.SQL_TEXT_CREATOR = :H AND A.SQL_PRODUCT = :H AND A.SQL_PANEL LIKE :H AND A.SQL_DEFAULT = 'Y'</pre>
</div>

##### Example 2:
Test output when specifying the minimum type of test parameters. Where the SQL Text for the statement executed under the program specified was not obtained.

###### JSON file input
```json
{
  "connection": {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11b"
  },
  "tests": 
  [
    {
      "test_type": "sql text",
      "environment": "R20",
      "product_code": "PDT",
      "current_vcat": "PDTDBA.R19",
      "current_datastore": "QATEST19",
      "current_interval_date": "1",
      "current_interval_time": "20:37:26",
      "plan": "RCUUD190",
      "program": "PTASSPI",
      "collid": "AUTHD190_BSSP"
    }
  ]
}
```

###### Report Output

<div style="overflow:scroll;overflow-x:hidden;overflow-y:hidden">

    <pre>-----------------------------------------------------------------------------------
         2017-08-21                               SQL Text Captured Report          14:42:07
         2017-08-21-14:42:07, PLAN:  DISTSERV
         
         2017-08-21-14:42:07, PROGRAM:  SYSSTAT 
         
         2017-08-21-14:42:07, SQL_CALL STMT#    SECT#    TEXT CAPTURED BY PRODUCT
         2017-08-21-14:42:07, -------- -------- -------- -------------------------
         2017-08-21-14:42:07, CALLSTMT 0000002  00002     </pre>                                      
</div>

#### Example Output for Test 2

##### Example 1:
Test output when specifying a list of source SQL text. Where the SQL Text for all the statements executed under the program(s) specified matched the source SQL text. 

###### JSON file input
<div style="overflow:scroll;overflow-x:hidden;overflow-y:hidden;width:200%">

```json
{
  "connection": {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11b"
  },
  "tests": 
  [
    {
      "test_type": "sql text",
      "environment": "R20",
      "product_code": "PDT",
      "current_vcat": "PDTDBA.R19",
      "current_datastore": "QATEST19",
      "current_interval_date": "1",
      "current_interval_time": "20:37:26",
      "plan": "DISTSERV",
      "program": "ALL",
      "text_type": "dynamic",
      "text list":
      {
        "text1": "SELECT  COUNT ( * ) FROM SYSIBM.SYSPACKAGE",
        "text2": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'T'",
        "text3": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'V'",
        "text4": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'A'",
        "text5": "SELECT  COUNT ( DISTINCT CREATOR ) FROM SYSIBM.SYSTABLES",
        "text6": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLESPACE",
        "text7": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'M'",
        "text8": "SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'F'",
        "text9": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSTRIGGERS' AND TBCREATOR = 'SYSIBM'",
        "text10": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSVIEWS' AND TBCREATOR = 'SYSIBM'",
        "text11": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'CREATESTMT' AND TBNAME = 'SYSROUTINES_SRC' AND TBCREATOR = 'SYSIBM'",
        "text12": "SELECT  COUNT ( * ) FROM SYSIBM.SYSINDEXES",
        "text13": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTABCONST",
        "text14": "SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'P'",
        "text15": "SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'STMT' AND TBNAME = 'SYSPACKSTMT' AND TBCREATOR = 'SYSIBM'",
        "text16": "SELECT  COUNT ( * ) FROM SYSIBM.SYSSYNONYMS",
        "text17": "SELECT  COUNT ( * ) FROM SYSIBM.SYSDATATYPES WHERE OWNERTYPE = ''",
        "text18": "SELECT  COUNT ( * ) FROM SYSIBM.SYSTRIGGERS",
        "text19": "SELECT  COUNT ( * ) FROM SYSIBM.SYSSEQUENCES",
        "text20": "SELECT  COUNT ( * ) FROM SYSIBM.XSROBJECTS"
      }
    }
  ]
}
```

</div>

###### Report Output

<div style="overflow:scroll;overflow-x:hidden;overflow-y:hidden;width:275%">

    <pre>-----------------------------------------------------------------------------------
         2017-08-21                               SQL Text Captured Report          14:42:56
         2017-08-21-14:42:56, PLAN:  DISTSERV
         
         2017-08-21-14:42:56, PROGRAM:  SYSLH200
         
         2017-08-21-14:42:56, SQL_CALL STMT#    SECT#    TEXT CAPTURED BY PRODUCT                                                                                                    MATCHED USER SUPPLIED TEXT                                                                                                 
         2017-08-21-14:42:56, -------- -------- -------- --------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSPACKAGE                                                                                  SELECT  COUNT ( * ) FROM SYSIBM.SYSPACKAGE
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'T'                                                                  SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'T'
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'V'                                                                  SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'V'
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'A'                                                                  SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'A'
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( DISTINCT CREATOR ) FROM SYSIBM.SYSTABLES                                                                    SELECT  COUNT ( DISTINCT CREATOR ) FROM SYSIBM.SYSTABLES
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLESPACE                                                                               SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLESPACE
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'M'                                                                  SELECT  COUNT ( * ) FROM SYSIBM.SYSTABLES WHERE TYPE = 'M'
         2017-08-21-14:42:56, PREPARE  0000001  00001    SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'F'                                                         SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'F'
         2017-08-21-14:42:56, PREPARE  0000001  00001    SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSTRIGGERS' AND TBCREATOR = 'SYSIBM'           SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSTRIGGERS' AND TBCREATOR = 'SYSIBM'
         2017-08-21-14:42:56, PREPARE  0000001  00001    SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSVIEWS' AND TBCREATOR = 'SYSIBM'              SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'TEXT' AND TBNAME = 'SYSVIEWS' AND TBCREATOR = 'SYSIBM'
         2017-08-21-14:42:56, PREPARE  0000001  00001    SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'CREATESTMT' AND TBNAME = 'SYSROUTINES_SRC' AND TBCREATOR = 'SYSIBM' SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'CREATESTMT' AND TBNAME = 'SYSROUTINES_SRC' AND TBCREATOR = 'SYSIBM'
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSINDEXES                                                                                  SELECT  COUNT ( * ) FROM SYSIBM.SYSINDEXES
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSTABCONST                                                                                 SELECT  COUNT ( * ) FROM SYSIBM.SYSTABCONST
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'P'                                                         SELECT  COUNT ( * ) FROM SYSIBM.SYSROUTINES WHERE ROUTINETYPE = 'P'
         2017-08-21-14:42:56, PREPARE  0000001  00001    SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'STMT' AND TBNAME = 'SYSPACKSTMT' AND TBCREATOR = 'SYSIBM'           SELECT  FOREIGNKEY FROM SYSIBM.SYSCOLUMNS WHERE NAME = 'STMT' AND TBNAME = 'SYSPACKSTMT' AND TBCREATOR = 'SYSIBM'
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSSYNONYMS                                                                                 SELECT  COUNT ( * ) FROM SYSIBM.SYSSYNONYMS
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSDATATYPES WHERE OWNERTYPE = ''                                                           SELECT  COUNT ( * ) FROM SYSIBM.SYSDATATYPES WHERE OWNERTYPE = ''
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSTRIGGERS                                                                                 SELECT  COUNT ( * ) FROM SYSIBM.SYSTRIGGERS
         2017-08-21-14:42:56, PREPARE  0000002  00002    SELECT  COUNT ( * ) FROM SYSIBM.SYSSEQUENCES                                                                                SELECT  COUNT ( * ) FROM SYSIBM.SYSSEQUENCES
         2017-08-21-14:42:56, PREPARE  0000001  00001    SELECT  COUNT ( * ) FROM SYSIBM.XSROBJECTS                                                                                  SELECT  COUNT ( * ) FROM SYSIBM.XSROBJECTS</pre>                                      
</div>

##### Example 2:
Test output when specifying a list of source SQL text. Where the SQL Text for all the statement executed under the program specified did not match any of the source SQL text provided and none of the SQL test in the user provided list list so a SQL Text not Found report is printed.

###### JSON file input
```json
{
  "connection": {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11b"
  },
  "tests": 
  [
    {
      "test_type": "sql text",
      "environment": "R20",
      "product_code": "PDT",
      "current_vcat": "PDTDBA.R19",
      "current_datastore": "QATEST19",
      "current_interval_date": "1",
      "current_interval_time": "20:37:26",
      "plan": "DISTSERV",
      "program": "SYSSTAT",
      "collid": "NULLID",
      "text_type": "dynamic",
      "text list":
      {
        "text1": "CALL PROGRAM"
      }
    }
  ]
}
```

###### Report Output

<div style="overflow:scroll;overflow-x:hidden;overflow-y:hidden">

    <pre>-----------------------------------------------------------------------------------
    2017-08-21                               SQL Text Captured Report          14:44:48
    2017-08-21-14:44:48, PLAN:  DISTSERV
    
    2017-08-21-14:44:48, PROGRAM:  SYSSTAT 
    
    2017-08-21-14:44:48, SQL_CALL STMT#    SECT#    TEXT CAPTURED BY PRODUCT  MATCHED USER SUPPLIED TEXT
    2017-08-21-14:44:48, -------- -------- -------- ------------------------- -------------------------
    2017-08-21-14:44:48, CALLSTMT 0000002  00002     
    
    ------------------------------------------------------------------------------------
    2017-08-21                               SQL Text Not Found Report          14:44:48
    2017-08-21-14:44:48, USER KEY USER TEXT                                         
    2017-08-21-14:44:48, -------- --------------------------------------------------
    2017-08-21-14:44:48, text1    CALL PROGRAM                                      
    </prev>

</div>