: Run this after installing Anaconda3

: 1. Install Anaconda3 in user space (i.e. select "This user only" option) and open Anaconda Prompt
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
 
    python -m ipykernel install --user --name base --display-name "Python 3.6 (base)" 
 
: Modify the following line for different Anaconda3 installation directory
 
    set anaconda_dir=C:\Users\%username%\AppData\Local\Continuum\anaconda3
   
: Setup ArcGIS Pro Integration
 
: Setup new environment name - MODIFY THIS FOR DIFFERENT ENVIRONMENT NAME

    set environment_name=arcgispro-py3

:    Create Anaconda virtual environment for ArcGIS Pro integration:
    conda create -n %environment_name% python=3.6.6 numpy=1.13.3 matplotlib=2.0.2 scipy=0.19.1 pandas pyparsing xlrd xlwt spyder jupyter
 
:    Activate the newly-created environment:
    activate %environment_name%
 
:    Pin versions of specific packages to closely match ArcGIS Pro Python versions
    (echo python ==3.6.6 & echo numpy ==1.13.3 & echo matplotlib ==2.0.2 & echo scipy ==0.19.1) > %CONDA_PREFIX%\conda-meta\pinned
 
: Install ipykernel into new environment for environment-specific Jupyter notebook kernel
 
    conda install ipykernel --no-deps
 
: Manually create new iPython kernel spec for new environment
 
    python -m ipykernel install --user --name %environment_name% --display-name "Python 3.6 (%environment_name%)" 

:    Setup script to modify Python search paths
    mkdir C:\Users\%username%\AppData\Roaming\Python
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python36
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages
 
    cp usercustomise.py C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages
