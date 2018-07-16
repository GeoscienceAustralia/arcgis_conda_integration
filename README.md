# arcgis_conda_integration
This arcgis_conda_integration repo contains batch files and a Python script to link user-space Anaconda Python installations with either 32-bit ArcMap 10.5 or 64-bit ArcGIS Pro.

Modification of the Python installations bundled with ArcGIS is potentially dangerous, in that updates to module versions could break ArcPy. For this reason, the Python bundled with a packaged installation of ArcGIS  is usually locked-down and not able to be be extended or modified by users. The solution is to create a parallel installation of Anaconda Python in user-space, with package versions the same or close to the versions shipped with ArcGIS. 

The usercustomise.py script will append the Anaconda Python libraries from a Conda virtual environment to the search paths for ArcGIS Python when Python is invoked from ArcGIS, or, conversely, it will append the ArcGIS Python libraries from ArcGIS Python to the search paths for Anaconda when Python is invoked from Anaconda. This allows users to install and update packages more-or-less at will, and provides a safe way to test new packages.

# Installation
ArcMap 10.5 requires a user-space installation of the 32-bit version of Anaconda Python 2 (https://repo.anaconda.com/archive/Anaconda2-5.2.0-Windows-x86.exe). N.B: DO NOT INSTALL THE 64-BIT VERSION OF PYTHON 2 UNLESS ABSOLUTELY REQUIRED, AND THEN ONLY AFTER READING THE NOTE BELOW.

ArcGIS Pro  requires a user-space installation of the 64-bit version of Anaconda Python 3 (https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe). N.B: DO NOT INSTALL THE 32-BIT VERSION OF PYTHON 3.

Please perform the required installation(s) for your version(s) of ArcGIS, selecting the "Just Me" option to install in user-space (i.e. without requiring administrative privileges), and accept all other default options.

Note that you will need to separate the 32-bit and 64-bit versions of Python 2 if you require both on your system, since both installers will attempt to write to the one directory. Recommended practice in this case would be to add a "_32" or "_64" suffix to each default istallation directory in order to explicitly identify which is which. You will also need to adjust the CONDA_CONFIG section of usercustomize.py to be able to find the "Anaconda2_32" directory, since the default settings will look for the default "Anaconda2" directory.

After you have installed the required version(s) of Anaconda, download or clone this repo to a known directory, then open the "Anaconda Prompt" shortcut under the relevant version of Anaconda. At the resultant command line, change directory to the one containing these files, and then run the relevant batch file for the Anaconda version, i.e. prepare_anaconda2.bat for Anaconda2, or prepare_anaconda3.bat for Anaconda3. Each batch file will:
- update the base environment of Anaconda
- install some generally useful packages not included in the initial Anaconda installation to the base environment
- create a virtual environment with specific package versions for ArcGIS compatibility
- copy the usercustomize.py script to C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages

Note that if you are prompted for administrative access, just click "Cancel" - this is caused by some packages trying (erroneously) to write to the shared startup menu, and will not affect the actual installations or updates. Once the script has completed, you should be able to start the Anaconda Python, and enter "import arcpy" without error.
