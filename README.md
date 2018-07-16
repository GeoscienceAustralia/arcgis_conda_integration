# arcgis_conda_integration
This arcgis_conda_integration repo contains batch files and a Python script to link user-space Anaconda Python installations with either 32-bit ArcMap 10.5 or 64-bit ArcGIS Pro.

Modification of the Python installations bundled with ArcGIS is potentially dangerous, in that updates to module versions could break ArcPy. The solution is to create a parallel installation of Anaconda Python in user-space, with package versions the same or close to the versions shipped with ArcGIS. 

The usercustomise.py script will append the Anaconda Python libraries from a Conda virtual environment to the search paths for ArcGIS Python when Python is invoked from ArcGIS, or it will append the ArcGIS Python libraries from ArcGIS Python to the search paths for Anaconda when Python is invoked from Anaconda.

# Installation
ArcMap 10.5 requires a user-space installation of the 32-bit version of Anaconda Python 2 (https://repo.anaconda.com/archive/Anaconda2-5.2.0-Windows-x86.exe).

ArcGIS Pro  requires a user-space installation of the 64-bit version of Anaconda Python 3 (https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe).

Please perform the required user-space installation(s) for your version(s) of ArcGIS, selecting the "Just Me" option and accepting all other default options.

Note that you will need to separate the 32-bit and 64-bit versions of Python 2 if you require both on your system. Recommended practice in this case would be to add a "_32" or "_64" suffix to each default istallation directory in order to explicitly identify which is which. You will also need to adjust the CONDA_CONFIG section of usercustomize.py to be able to find the "Anaconda2_32" directory, since the default settings will look for the default "Anaconda2" directory.

After you have installed the required version(s) of Anaconda, download or clone this repo to a known directory, then open the "Anaconda Prompt" shortcut under the relevant version of Anaconda. Change directory to the one containing these files, and then run the relevant batch file for the Anaconda version, i.e. prepare_anaconda2.bat for Anaconda2, or prepare_anaconda3.bat for Anaconda3. Each batch file will:
- update Anaconda
- install some generally useful packages not included in the initial Anaconda installation
- create a virtual environment for ArcGIS compatibility
- copy the usercustomize.py script to C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages
