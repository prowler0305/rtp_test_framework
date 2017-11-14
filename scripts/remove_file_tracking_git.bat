::--------------------------------------------------------------------
::  Batch script to remove files from git that shouldn't be tracked.
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
:: Instructions:
:: 1. Duplicate the below command for as many files as you want to
::    untrack in one run.
::
:: 2. Replace <path> with the location of the file that should be
::    removed (i.e. right-click on file name in the Project window in
::    your IDE(e.g. IntelliJ) and click "Copy path"
::
::--------------------------------------------------------------------
%CMDER_GIT_HOME% update-index --assume-unchanged <path>
::--------------------------------------------------------------------
:: Exit Cmder
::--------------------------------------------------------------------
exit