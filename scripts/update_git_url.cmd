::--------------------------------------------------------------------
:: Set path variables so we can use Git commands
::--------------------------------------------------------------------
set CMDER_HOME="C:\cmder"
set CMDER_GIT_HOME="%CMDER_HOME%\vendor\git-for-windows\bin\git.exe"
setx CMDER_HOME %CMDER_HOME%
setx CMDER_GIT_HOME %CMDER_GIT_HOME%
::--------------------------------------------------------------------
:: Change into users INTELLIJ RTP master directory
::--------------------------------------------------------------------
cd %RTP_HOME%
::--------------------------------------------------------------------
:: Display current git url
::--------------------------------------------------------------------
%CMDER_GIT_HOME% config --get remote.origin.url
::--------------------------------------------------------------------
:: Change URL to new URL location
::--------------------------------------------------------------------
%CMDER_GIT_HOME% remote set-url origin https://github-isl-01.ca.com/DBMgmtModernization/RTP.git
::--------------------------------------------------------------------
:: Display new git url for verification
::--------------------------------------------------------------------
%CMDER_GIT_HOME% config --get remote.origin.url
