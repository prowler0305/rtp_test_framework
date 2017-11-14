# Automation Architecture and Design
---

This section contains information on the Python Automation (RTPPY) frameworks architecture and design. The architecture is composed in a way to provide a verbose keyword data driven user interface while simplifying and quickening the development of functionality expansion.

Overall the architecture uses a class-based hybrid inheritance structure which combines the concept of multilevel and hierarchical inheritance. It can be logically viewed as two entities, the class structures that provide the user interface(referred to as the front end) and the class structures that provide basic ISPF and product based functionality (referred to as the back end) which includes PTG2 functionality wrappers.

You can view [UML](https://cawiki.ca.com/display/DB2QA/Real+Time+Performance+Automation+Project#RealTimePerformanceAutomationProject-RTPUML) and [Flowchart](https://cawiki.ca.com/display/DB2QA/Real+Time+Performance+Automation+Project#RealTimePerformanceAutomationProject-HighLevelFlowChart) diagrams that visually show the class and program flow of the architecture.

## User Interface Architecture (Front End)

The front end architecture is designed around input from the user as a file written in JSON format and/or optional overriding command line arguments when invoking the main executable.

#### Builder
The Builder class is a static class that contain methods called by the main executable used to interact with the command line arguments and JSON file and most importantly create the correct "test type" BaseTest class instance which drives the rest of the execution.

#### InputParms
A static class that provides functionality for a class to retrieve test input parameters from the command line and/or JSON file. Also provide methods to raise an error or information message related to input parameters existence or non existence.

#### BaseTest
This is the highest class in the hierarchy in which all sub classes inherit from. Methods here are not particular to any one subclass. The Base Test classes build_test super method sets global class instance variables for those parameters that are needed across all tests(e.g. LPAR, USERID, SSID, etc.). Also provides generic methods like finding a value for a test input parameter using methods in the static InputParms class.

#### History
The history class inherits from the BaseTest class and is the base class in the hierarchical inheritance in which all test sub classes that interact with the products historical data displays inherit from either directly or indirectly. This class handles setting certain global class instance variables from the input parameters for those required and optional parameters needed by tests.

#### AggregateFactory
A static class who's only responsibility is to interrogate the "level" input parameter for a test from the JSON file in order to determine which Aggregate Compare sub class to create an instance of so that the Builder class and main can call the correct build_test and execute_test methods.

#### AggregateBase
This class while serving as a sub class in the hierarchical inheritance structure also serves as the base in another hierarchical inheritance structure for the below mentioned sub classes. The build_test method provided here overrides the History class build_test method in which the History class method is called as a super to ensure those parameters commonly handle by its parent are present. Then handles the required and optional parameters unique to an Aggregate Compare test. The execute_method handles the logic common across all aggregate sub classes that involves using the "back end" functionality to interact with the product displays.

Both the build_test and execute_test methods are overridden by its sub classes however are super called by the sub classes. All sub classes also have access to methods in the History and BaseTest classes through the AggregateBase classes inheritance.

##### AggregatePlan
Subclass that performs an aggregation of the program data and compares it to the plan data.

##### AggregateProgram
Subclass that performs an aggregation of the statement data and compares it to the program data.

##### AggregateKeys
Subclass that can aggregate either the plan or program data against the data for a user key.

#### IntervalCompare
This class inherits from the History class directly. It provides functionality that allows data at the interval summary level (i.e. View By level only) to be compared against a baseline and a current collection of the same executed SQL statements.

## Product based functionality (Back End)

As mentioned previously the RTPPY automation uses the PTG2 framework which is a python framework that provides the ability to navigate a mainframe emulator programmatically. The RTPPY framework wrappers simple and complex PTG2 services into ISPF and product based functionality for easier development. The design and architecture of the PTG2 framework is not discussed in detail here. If more information about PTG2 is wanted see the PTG2 Architecture wiki page.

The back end architecture is designed around providing classes and methods that encapsulate functionality around ISPF and product navigation, using the PTG2 architecture, and display data interaction.

#### CommonNav
Static class that contains a variety of methods around things like simple ISPF navigation (shift left, right, up, down, max up, max down, freeze and sort columns, etc....) that are non product specific. Also includes method for using PTG2 services for capturing a whole ISPF display.

#### NavRtp
This class contains encapsulates product functionality that is usable for all the RTP products (PDT/PSA/PTT) and is the base class that is inherited by the sub classes described below.

#### NavPdt
Subclass of NavRtp that encapsulates product functionality specific to Detector.

#### NavPsa
Subclass of NavRtp that encapsulates product functionality specific to Subsystem Analyzer.

#### RtpPrimaryKeys
A static class that provides information used by method(s) in the product Nav classes. The information is on the columns that should be used as primary keys when matching data rows for a specific or set of product displays.

#### Results
This class is composed by a method in the product Nav classes and is retained by a test class. The Results class encapsulates functionality to extract and interact with the columns and data on the product displays which is contained in the ColumnInfo class that is composed.

#### ColumnInfo
Class composed by the Results class that encapsulates the information about the columns and the data for a dynamic data area in the product displays.