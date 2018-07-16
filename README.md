# arcgis_conda_integration
This arcgis_conda_integration repo contains batch files and a Python script to link user-space Anaconda Python installations with either 32-bit ArcMap 10.5 or 64-bit ArcGIS Pro.

Modification of the Python installations bundled with ArcGIS is potentially dangerous, in that updates to module versions could break ArcPy. The solution is to create a parallel installation of Anaconda Python in user-space, with package versions the same or close to the versions shipped with ArcGIS. 

The usercustomise.py script will append the Anaconda Python libraries from a Conda virtual environment to the search paths for ArcGIS Python when Python is invoked from ArcGIS, or it will append the ArcGIS Python libraries from ArcGIS Python to the search paths for Anaconda when Python is invoked from Anaconda.

# Installation
ArcMap 10.5 requires a user-space installation of the 32-bit version of Anaconda Python 2 (https://repo.anaconda.com/archive/Anaconda2-5.2.0-Windows-x86.exe).

ArcGIS Pro  requires a user-space installation of the 64-bit version of Anaconda Python 3 (https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe).

Please perform the required user-space installation(s) for your version(s) of ArcGIS, selecting the "This user only" option and accepting all other default options.

Download or clone this repo to a known directory, then open the "Anaconda Prompt" shortcut under the relevant version of Anaconda. Change directory to the one containing these files, and then run the relevant batch file for the Anaconda version, i.e. prepare_anaconda2.bat for Anaconda2, or prepare_anaconda3.bat for Anaconda3.
