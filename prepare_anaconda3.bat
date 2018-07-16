: Install 64-bit Anaconda3 in user space (i.e. select "Just Me" option) and open Anaconda Prompt
: Run this batch file from the command line

: Try updating conda itself:
    call conda update --yes conda

: Try updating all packages:
    call conda update --yes --all

: Perform the following "conda install" for generally useful packages to install them into base environment:

    call conda install --yes GDAL PyProj Shapely cx_Oracle netcdf4 owslib xarray cartopy pandas pyparsing xlrd xlwt 

: Manually create new iPython kernel spec for base environment
:    python -m ipykernel install --user --name base --display-name "Python 3.6 (base)" 

: Modify the following line for different Anaconda2 installation directory
    set anaconda_dir=C:\Users\%username%\AppData\Local\Continuum\anaconda3


: Setup ArcGIS Desktop Integration

: Setup new environment name - MODIFY THIS FOR DIFFERENT ENVIRONMENT NAME
    set environment_name=arcgispro-py3

: Attempt to delete any pre-existing environment with this name
	call conda env remove --yes --name %environment_name%

: Create Anaconda virtual environment for ArcGIS Desktop integration:
    call conda create --yes --name %environment_name% python=3.6.6 numpy=1.13.3 matplotlib=2.0.2 scipy=0.19.1 spyder jupyter

: Activate the newly-created environment:
    call activate %environment_name%

: Pin versions of specific packages to closely match ArcGIS Desktop Python versions
    (echo python ==3.6.6 & echo numpy ==1.13.3 & echo matplotlib ==2.0.2 & echo scipy ==0.19.1) > %CONDA_PREFIX%\conda-meta\pinned

: Install ipykernel into new environment for environment-specific Jupyter notebook kernel
:    call conda install ipykernel --no-deps

: Manually create new iPython kernel spec for new environment
:    python -m ipykernel install --user --name %environment_name% --display-name "Python 3.6 (%environment_name%)" 

: Setup script to modify Python search paths
    mkdir C:\Users\%username%\AppData\Roaming\Python
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python36
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages
    copy usercustomize.py C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages
