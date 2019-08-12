: Install Anaconda2 in user space (i.e. select "Just Me" option) and open Anaconda Prompt
: Run this batch file from the command line

: Try updating conda itself:
    call conda update --yes conda

: Try updating all packages:
    call conda update --yes --all

: Perform the following "conda install" for generally useful packages to install them into base environment:
:    call conda install --yes GDAL PyProj Shapely cx_Oracle netcdf4 owslib xarray cartopy pandas pyparsing xlrd xlwt 

: Modify the following line for different Anaconda2 installation directory
    set anaconda_dir=C:\Users\%username%\AppData\Local\Continuum\anaconda2


: Setup ArcGIS Desktop Integration

: Setup new environment name - MODIFY THIS FOR DIFFERENT ENVIRONMENT NAME
    set environment_name=arc106_32bit

: Attempt to delete any pre-existing environment with this name
    call conda env remove --yes --name %environment_name%

: Create Anaconda virtual environment for ArcGIS Desktop integration:
    call conda create --yes --name %environment_name% cycler=0.10.0 mpmath=0.19 nose=1.3.7 numpy=1.9.3 python=2.7.14 six=1.10.0 spyder jupyter

: Activate the newly-created environment:
    call activate %environment_name%

: Pin versions of specific packages to closely match ArcGIS Desktop Python versions
    copy /Y argis_desktop_pinned.txt %CONDA_PREFIX%\conda-meta\pinned

: Setup script to modify Python search paths
    mkdir C:\Users\%username%\AppData\Roaming\Python
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python27
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python27\site-packages
    copy /Y usercustomize.py C:\Users\%username%\AppData\Roaming\Python\Python27\site-packages
