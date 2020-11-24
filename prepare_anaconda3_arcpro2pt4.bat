:: Install 64-bit Anaconda3 in user space (i.e. select "Just Me" option) and open Anaconda Prompt
:: Run this batch file from the command line

:: Setup ArcGIS Desktop Integration without upgrading the Conda install

:: Add additional channels.  Adding a channel pushes it to the top priority in the list, hence conda-forge is done after Esri so it has higher priority
    call conda config --add channels Esri
    call conda config --add channels conda-forge

:: Setup new environment name - MODIFY THIS FOR DIFFERENT ENVIRONMENT NAME
    set environment_name=arcgispro2pt4-py3

:: Attempt to delete any pre-existing environment with this name
    call conda env remove --yes --name %environment_name%

:: Create Anaconda virtual environment for ArcPro 2.4 integration.  Python version matches Pro2.4
    call conda create --yes --name %environment_name% python=3.6.8

:: Activate the newly-created environment::
    call activate %environment_name%

:: Create Anaconda virtual environment for ArcPro 2.4 integration
    call conda install --yes arcgis=1.6.1 asn1crypto=0.24.0 atomicwrites=1.3.0 attrs=19.1.0 backcall=0.1.0 bleach=3.1.0 certifi=2019.3.9 cffi=1.12.2 cftime=1.0.0b1 chardet=3.0.4 colorama=0.4.1 cryptography=2.6.1 cycler=0.10.0 decorator=4.4.0 defusedxml=0.5.0 despatch=0.1.0 entrypoints=0.3 et_xmlfile=1.0.1 fastcache=1.0.2 future=0.17.1 h5py=2.9.0 html5lib=1.0.1 idna=2.8 ipykernel=5.1.0 ipython_genutils=0.2.0 ipython=7.4.0 ipywidgets=7.4.2 jdcal=1.4 jedi=0.13.3 jinja2=2.10.1 jsonschema=3.0.1 jupyter_client=5.2.4 jupyter_console=6.0.0 jupyter_core=4.4.0 jupyterlab_server=0.2.0 jupyterlab=0.35.4 keyring=19.0.1 kiwisolver=1.0.1 markupsafe=1.1.1 matplotlib=3.0.3 mistune=0.8.4 mkl_fft=1.0.10 mkl_random=1.0.2 more-itertools=6.0.0 mpmath=1.1.0 nbconvert=5.4.1 nbformat=4.4.0 netcdf4=1.5.0.1 nose=1.3.7 notebook=5.7.8 numexpr=2.6.9 numpy=1.16.2 openpyxl=2.6.1 pandas=0.24.2 pandocfilters=1.4.2 parso=0.3.4 pickleshare=0.7.5 pip=19.0.3 pluggy=0.9.0 prometheus_client=0.6.0 prompt_toolkit=2.0.9 py=1.8.0 pycparser=2.19 pygments=2.3.1 pyopenssl=19.0.0 pyparsing=2.4.0 pyrsistent=0.14.11 pyshp=1.2.12 pysocks=1.6.8 pytest=4.4.0 python-dateutil=2.8.0 pytz=2018.9 pywin32-ctypes=0.2.0 pywinpty=0.5 pyzmq=18.0.0 requests=2.21.0 scipy=1.2.1 send2trash=1.5.0 setuptools=41.0.0 simplegeneric=0.8.1 six=1.12.0 sympy=1.3 terminado=0.8.1 testpath=0.4.2 tornado=6.0.2 traitlets=4.3.2 urllib3=1.24.1 wcwidth=0.1.7 webencodings=0.5.1 wheel=0.33.1 widgetsnbextension=3.4.2 win_inet_pton=1.1.0 wincertstore=0.2 winkerberos=0.7.0 x86cpu=0.4 xlrd=1.2.0 xlwt=1.3.0 jupyter spyder	

:: Setup script to modify Python search paths for Python 3.6
    mkdir C::\Users\%username%\AppData\Roaming\Python
    mkdir C::\Users\%username%\AppData\Roaming\Python\Python36
    mkdir C::\Users\%username%\AppData\Roaming\Python\Python36\site-packages
    copy /Y usercustomize.py C::\Users\%username%\AppData\Roaming\Python\Python36\site-packages
