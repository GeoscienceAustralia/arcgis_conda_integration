: Install 64-bit Anaconda3 in user space (i.e. select "Just Me" option) and open Anaconda Prompt
: Run this batch file from the command line

: Try updating conda itself:
    call conda update --yes conda

: Try updating all packages:
    call conda update --yes --all

: Perform the following "conda install" for generally useful packages to install them into base environment:

    call conda install --yes GDAL PyProj Shapely cx_Oracle netcdf4 owslib xarray cartopy pandas pyparsing xlrd xlwt 

: Modify the following line for different Anaconda2 installation directory
    set anaconda_dir=C:\Users\%username%\AppData\Local\Continuum\anaconda3


: Setup ArcGIS Desktop Integration

: Setup new environment name - MODIFY THIS FOR DIFFERENT ENVIRONMENT NAME
    set environment_name=arcgispro-py3

: Attempt to delete any pre-existing environment with this name
    call conda env remove --yes --name %environment_name%

: Create Anaconda virtual environment for ArcGIS Desktop integration:
    call conda create --yes --name %environment_name% asn1crypto=0.24.0 attrs=17.4.0 backcall=0.1.0 bleach=2.1.3 ca-certificates=2018.03.07 certifi=2018.1.18 cffi=1.11.5 chardet=3.0.4 colorama=0.3.9 cryptography=2.2.2 cycler=0.10.0 decorator=4.2.1 entrypoints=0.2.3 et_xmlfile=1.0.1 freetype=2.8 future=0.16.0 html5lib=1.0.1 idna=2.6 intel-openmp=2018.0.0 ipykernel=4.8.2 ipython=6.3.1 ipython_genutils=0.2.0 ipywidgets=7.2.1 jdcal=1.4 jedi=0.11.1 jinja2=2.10 jsonschema=2.6.0 jupyter_client=5.2.3 jupyter_core=4.4.0 keyring=11.0.0 kiwisolver=1.0.1 libpng=1.6.34 markupsafe=1.0 matplotlib=2.2.2 mistune=0.8.3 mkl=2018.0.2 mkl_fft=1.0.1 mkl_random=1.0.1 more-itertools=4.1.0 mpmath=1.0.0 nbconvert=5.3.1 nbformat=4.4.0 netcdf4=1.3.1 nose=1.3.7 notebook=5.4.1 numexpr=2.6.4 numpy=1.14.2 openpyxl=2.5.2 openssl=1.0.2o pandas=0.22.0 pandocfilters=1.4.2 parso=0.1.1 pickleshare=0.7.4 pip=9.0.3 pluggy=0.6.0 prompt_toolkit=1.0.15 py=1.5.3 pycparser=2.18 pygments=2.2.0 pyopenssl=17.5.0 pyparsing=2.2.0 pysocks=1.6.8 pytest=3.5.0 python=3.6.5 python-dateutil=2.7.2 pytz=2018.3 pywinpty=0.5 pyzmq=17.0.0 requests=2.18.4 scipy=1.0.1 send2trash=1.5.0 setuptools=39.0.1 simplegeneric=0.8.1 six=1.11.0 sympy=1.1.1 terminado=0.8.1 testpath=0.3.1 tornado=5.0.2 traitlets=4.3.2 urllib3=1.22 vc=14 vs2015_runtime=14.0.25420 wcwidth=0.1.7 webencodings=0.5.1 wheel=0.31.0 widgetsnbextension=3.2.1 win_inet_pton=1.0.1 wincertstore=0.2 winkerberos=0.7.0 winpty=0.4.3 xlrd=1.1.0 xlwt=1.3.0 zlib=1.2.11 jupyter spyder

: Activate the newly-created environment:
    call activate %environment_name%

: Pin versions of specific packages to closely match ArcGIS Desktop Python versions
    copy /Y argis_pro_pinned.txt %CONDA_PREFIX%\conda-meta\pinned

: Setup script to modify Python search paths for Python 3.6
    mkdir C:\Users\%username%\AppData\Roaming\Python
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python36
    mkdir C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages
    copy /Y usercustomize.py C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages
