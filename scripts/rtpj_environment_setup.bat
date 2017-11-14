::--------------------------------------------------------------------
::  RTPJ Environment Setup script
::  Instructions:
::  1.) Make a copy of this script in the scripts/custom directory.
::  2.) replace the <path> variables where indicated below.
::--------------------------------------------------------------------

::--------------------------------------------------------------------
:: a. Replace <path> with the location of the JDBC drivers:
::  db2jcc_license_cisuz.jar and  db2jcc4.jar
::--------------------------------------------------------------------
setx JDBC_DRIVERS "<path>"

::--------------------------------------------------------------------
:: b. Replace <path> with the location of the RTP project directory.
::  Example: C:\Users\bergr05\IdeaProjects\rtp
::--------------------------------------------------------------------
setx RTP_HOME "<path>"

::--------------------------------------------------------------------
:: c.  Replace <path> with the location of the JAVA SDK.
::   Example: C:\Program Files\Java\jdk1.8.0_74
::--------------------------------------------------------------------
setx JAVA_HOME "<path>"

::--------------------------------------------------------------------
:: d. Replace <path> with the location of the Maven directory.
::  Internal intellij example:
::  C:\Program Files (x86)\JetBrains\IntelliJ IDEA 2016.1\plugins\maven\lib\maven3
::--------------------------------------------------------------------
setx MAVEN_HOME "<path>"

::--------------------------------------------------------------------
:: e. Replace <path> with the location of Cmder.exe file
::--------------------------------------------------------------------
setx CMDER_HOME "<path>"
setx CMDER_GIT_HOME "%CMDER_HOME%\vendor\git-for-windows\bin\git.exe"

exit