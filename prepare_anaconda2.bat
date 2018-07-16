: Run this after installing Anaconda2

: 1. Install Anaconda2 in user space (i.e. select "This user only" option) and open Anaconda Prompt
: 2. Try updating conda itself:
 
    conda update conda
 
: 3. Try updating all packages:
 
    conda update --all
 
: 4. Retry any failed packages individually (e.g. "conda update ipykernel")
: 5. Repeat 3-4 until "All requested packages already installed" (if required)
: 6. Optionally perform the following "conda install" steps for generally useful packages to install them into base environment:
 
    conda install GDAL
    conda install PyProj
    conda install Shapely
    conda install cx_Oracle
    conda install netcdf4
    conda install owslib
    conda install xarray
    conda install cartopy
 
: Manually create new iPython kernel spec for base environment

    python -m ipykernel install --user --name base --display-name "Python 2.7 (base)" 

: Modify the following line for different Anaconda2 installation directory

    set anaconda_dir=C:\Users\%username%\AppData\Local\Continuum\anaconda2

: Setup ArcGIS Desktop Integration

: Setup new environment name - MODIFY THIS FOR DIFFERENT ENVIRONMENT NAME

    set environment_name=_arc105_32bit

:    Create Anaconda virtual environment for ArcGIS Desktop integration:
    conda create -n %environment_name% python=2.7.12 numpy=1.11.2 matplotlib=1.5.3 scipy=0.17.0 pandas pyparsing xlrd xlwt spyder jupyter

:    Activate the newly-created environment:
    activate %environment_name%

:    Pin versions of specific packages to closely match ArcGIS Desktop Python versions
    (echo python ==2.7.12 & echo numpy ==1.11.2 & echo matplotlib ==1.5.3 & echo scipy ==0.17.0) > %CONDA_PREFIX%\conda-meta\pinned

: Install ipykernel into new environment for environment-specific Jupyter notebook kernel

    conda install ipykernel --no-deps

: Manually create new iPython kernel spec for new environment

    python -m ipykernel install --user --name %environment_name% --display-name "Python 2.7 (%environment_name%)" 

:    Setup script to modify Python search paths
    mkdir C:\Users\%username%\AppData\Roaming\Python
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python27
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python27\site-packages

    cp usercustomize.py C:\Users\%username%\AppData\Roaming\Python\Python27\site-packages
