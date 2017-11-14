# Lock Release

**WARNING WARNING WARNING!!! This test can cause DB2 to crash**

This test type allows testing of the Detector collection engines ability to release a CML Lock that was obtained during
 interval switch building the new interval collection buckets but was not released during normal flow.
 
This is accomplished by zapping two instructions in the correct version of DT$DIU for the DB2 Version the PDT collection
will be started for. Code snippets follow:

1) The J and JZ instructions at offsets B9A and BA0 are found by looking for the LGR and CDSG instruction set.
```
00000B8C B904 00F7                         15573+         LGR   R15,R7                       SET NEW ANCHOR ADDR        
00000B90 EB0E 6010 003E          00000010  15574+         CDSG  R0,R14,STM$SANC              INSERT NEW ENTRY           
00000B96 A774 FFF4               00000B7E  15575+         JNE   A0932                        TRY AGAIN                  
00000B9A A7F4 0005               00000BA4  15576          J     UPDT2400                                             
                                           15577 *                                                                      
00000B9E                                   15578 UPDT2350 DS    0H                                                      
00000B9E 1222                              15579          LTR   R2,R2                        DO WE HAVE LOCK         
00000BA0 A784 0009               00000BB2  15580          JZ    UPDT2450                     ..NO, THEN SKIP THIS    
```
2) The unconditional J instruction (offset B9A) is zapped to a NOP while the JZ instruction (offset BA0) is zapped to an
   unconditional J to UPDT2450 which branches around the call to DT$IURLK(i.e. BAKR at BAE) to release the CML Lock.
```
B8C B904 00F7                   LGR      RW15,RW7           
B90 EB0E 6010 003E              CDSG     R0,R14,X'00010'(R6)
B96 A774 FFF4                   JNE      *-X'0018'            (PTX0004:PDTDIUC0.DT$DIUC0+B7E)
B9A 4700 0005                   NOP      X'005'                                              
B9E 1222                        LTR      R2,R2                                               
BA0 A7F4 0009                   J        *+X'0012'            (PTX0004:PDTDIUC0.DT$DIUC0+BB2)
BA4 4110 C000                   LA       R1,X'000'(,R12)                                     
BA8 E3F0 A118 0017              LLGT     RW15,X'00118'(,R10)                                 
BAE B240 000F                   BAKR     0,R15                                               
BB2 E370 C510 0024              STG      RW7,X'00510'(,R12)                                            
```


Because of the nature of this test altering code in collection engine modules that are directly execute by threads in the DB2
address space and/or modules that remain loaded for the duration of the xmanager address space. It is highly suggested that users
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
column. Additionally there are [examples](#json-example) at the bottom of this page.

#### Required
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[product_code](json-parameters.md#product_code) |
[test_type](json-parameters.md#test_type) |
[lpar](json-parameters.md#lpar) | [lpar](command-line-options.md#lpar)
[userid](json-parameters.md#userid) | [userid](command-line-options.md#userid)
[ssid](json-parameters.md#ssid) | [ssid](command-line-options.md#ssid)
[xman](json-parameters.md#xman) | [xman](command-line-options.md#xman)

#### Optional
JSON | Command Line Override | Special Usage or Note
---- | --------------------- | ---------------------
[output_location](json-parameters.md#output_location) | [output_location](command-line-options.md#output_location)

# JSON Example
---

```json
{
  "connection":
  {
    "lpar": "ca11",
    "userid": "qartp01",
    "ssid": "d11c"
  },
  "tests":
  [
    {
      "description": "Zap instructions in DT$DIU so that DIU does not release the CML lock",
      "test_type": "lock release",
      "product_code": "PDT",
      "environment": "",
      "xman": "ptx0004"
    }
  ]
}

```