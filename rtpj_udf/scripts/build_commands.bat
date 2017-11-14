erase ftpJar.bat
echo open usilca11.ca.com >>ftpJar.bat
echo qadba01 >>ftpJar.bat
echo <pw> >>ftpJar.bat
echo prompt off >>ftpJar.bat
echo binary >>ftpJar.bat

echo cd /u/users/db2mf20/rtpJars >>ftpJar.bat
echo lcd "%RTP_HOME%\rtpj_udf\target" >>ftpJar.bat

echo put rtpj_udf-1.0-SNAPSHOT.jar >>ftpJar.bat

echo quit >> ftpJar.bat
