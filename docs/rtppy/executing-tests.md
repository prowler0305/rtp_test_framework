# Executing Python Test Scripts
---
## Main Execution
The main test driver, **ISPFTest.py**, serves as the main entry point for the RTPPY framework. This main script uses Builder
class methods to parse the command line argument overrides and/or input file in JSON format specified.

## Execute Command
The following command is used to invoke the main test driver, of which requires the -f or --file command to indicate the name
of the input JSON file that contains the test or tests and it's parameters needed to execute.

```
python ISPFTest.py --file=inputfile
```

### How to create tests
See [Creating Tests](creating-tests.md) on how to write tests using the existing framework with the JSON structure.

---
## How do I execute tests?
Tests can be executed either locally on your machine [via Intellij](execute-intellij.md) or [via Jenkins](execute-jenkins.md) with preset builds setup.