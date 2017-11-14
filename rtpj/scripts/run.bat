::
:: This windows batch script executes the rtpj-1.0SNAPSHOT.jar file.
::

::---------------------------------------------------------------
:: Use this section to specify the test and optional parameters.
:: Set the test to execute

set RTP_TEST=RTPJ_Full_Suite.JSON

:: Set the command line parameters (optional)

set RTP_PARMS=--SSID=DB0G

::---------------------------------------------------------------

:: Move to the location of the jar file.
cd "%RTP_HOME%\rtpj\target"

:: Set the classpath
set CLASSPATH=%JDBC_DRIVERS%\*;%RTP_HOME%\rtpj\target\rtpj-1.0-SNAPSHOT.jar;%CLASSPATH%

:: Execute THE TEST
java com.ca.rtp.core.JsonTestRunner %RTP_TEST% %RTP_PARMS%


::---------------------------------------------------------------
:: Other commands
:: Example for overriding the log4j configuration.
::java -Dlog4j.configurationFile=file:\%RTP_HOME%\rtpj\rtpj_log4j2_config.xml com.ca.rtp.core.JsonTestRunner Basic_Select_Test.JSON

:: Example for setting the CLASSPATH inline with the execution command
:: java -cp "%JDBC_DRIVERS%\*";"%RTP_HOME%\rtpj\target\rtpj-1.0-SNAPSHOT.jar" com.ca.rtp.core.JsonTestRunner %RTP_TEST% %RTP_PARMS%
::---------------------------------------------------------------
