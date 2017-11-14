::--------------------------------------------------------------------
:: Change all 3 RTP automation Mainframe ID passwords
::--------------------------------------------------------------------
ptg-auth --system tpx --userid qartp01 --set QARTP17
ptg-auth --system tpx --userid qartp02 --set QARTP17
ptg-auth --system tpx --userid qartp03 --set QARTP17
::--------------------------------------------------------------------
:: Display newly changed passwords for verification
::--------------------------------------------------------------------
ptg-auth --system tpx --userid qartp01
ptg-auth --system tpx --userid qartp02
ptg-auth --system tpx --userid qartp03
