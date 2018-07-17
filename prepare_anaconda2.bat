: Install Anaconda2 in user space (i.e. select "Just Me" option) and open Anaconda Prompt
: Run this batch file from the command line

: Try updating conda itself:
    call conda update --yes conda

: Try updating all packages:
    call conda update --yes --all

: Perform the following "conda install" for generally useful packages to install them into base environment:

    call conda install --yes GDAL PyProj Shapely cx_Oracle netcdf4 owslib xarray cartopy pandas pyparsing xlrd xlwt 

: Manually create new iPython kernel spec for base environment
:    python -m ipykernel install --user --name base --display-name "Python 2.7 (base)" 

: Modify the following line for different Anaconda2 installation directory
    set anaconda_dir=C:\Users\%username%\AppData\Local\Continuum\anaconda2


: Setup ArcGIS Desktop Integration

: Setup new environment name - MODIFY THIS FOR DIFFERENT ENVIRONMENT NAME
    set environment_name=arc105_32bit

: Attempt to delete any pre-existing environment with this name
    call conda env remove --yes --name %environment_name%

: Create Anaconda virtual environment for ArcGIS Desktop integration:
    call conda create --yes --name %environment_name% python=2.7.12 numpy=1.11.2 matplotlib=1.5.3 scipy=0.17.0 spyder jupyter

: Activate the newly-created environment:
    call activate %environment_name%

: Pin versions of specific packages to closely match ArcGIS Desktop Python versions
    (echo python ==2.7.12 & echo numpy ==1.11.2 & echo matplotlib ==1.5.3 & echo scipy ==0.17.0) > %CONDA_PREFIX%\conda-meta\pinned

: Install ipykernel into new environment for environment-specific Jupyter notebook kernel
:    call conda install ipykernel --no-deps

: Manually create new iPython kernel spec for new environment
:    python -m ipykernel install --user --name %environment_name% --display-name "Python 2.7 (%environment_name%)" 

: Setup script to modify Python search paths
    mkdir C:\Users\%username%\AppData\Roaming\Python
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python27
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python27\site-packages
    copy /Y usercustomize.py C:\Users\%username%\AppData\Roaming\Python\Python27\site-packages
