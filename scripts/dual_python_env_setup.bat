::--------------------------------------------------------------------
::  RTPPY Dual Python Version Environment Setup script
::  Instructions:
::--------------------------------------------------------------------

conda create -y --name workshop  python=3.5

call activate workshop

conda install -y lxml

conda install -y -c conda-forge jpype1

pip install --index-url http://dm/pip --trusted-host dm JPype1 "numpy<2"

pip install --extra-index-url http://dm.ca.com/pip --trusted-host dm.ca.com ptg2
