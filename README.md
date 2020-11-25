# arcgis_conda_integration
This arcgis_conda_integration repo contains batch files and a Python script to link parallel user-space Anaconda Python installations with either 32-bit ArcMap or 64-bit ArcGIS Pro.

Modification of the Python installations bundled with ArcGIS is potentially dangerous, in that updates to module versions could break ArcPy, sometimes requiring a full rebuild of the user environment. For this reason, the Python bundled with a packaged installation of ArcGIS  is usually locked-down and not able to be be extended or modified by users without administrative privileges. A solution is to create a parallel installation of Anaconda Python in user-space, with package versions the same or close to the versions shipped with ArcGIS, and manage the search lists to allow Conda to access ArcGIS libraries and vice versa.

The usercustomise.py script in this repo will append the Anaconda Python libraries from a Conda virtual environment to the search paths for ArcGIS Python when Python is invoked from ArcGIS, or, conversely, it will append the ArcGIS Python libraries from ArcGIS Python to the search paths for Anaconda when Python is invoked from Anaconda. This allows users to install and update packages more-or-less at will, and provides a safe way to test new packages in Conda virtual environments.


# Revisions

| Date       | Author     | Comment                               |
|------------|------------|---------------------------------------|
| 25/11/2020 | R. Coghlan | Added new batch script for ArcPro 2.4, Updated readme.md to include python module updates |



# ArcGIS/ArcPro version updates

The batch files supplied in this repo can be updated to work on various version of ArcGIS/ArcPro.  To do so, a list of module dependcies must be extracted from the Arc version you are using and then the batch file copied/updated to reference these new versions.
To generate a list of python modules, in the python window in either ArcMap or ArcPro paste the following;

	import pkg_resources
	installed_packages = pkg_resources.working_set
	installed_packages_list = sorted(["%s=%s" % (i.key, i.version) for i in installed_packages])
	print(" ".join(installed_packages_list))

The returned string can be copied into either a new or existing batch script and will replace the existing package list. 

The python version will also have to be updated in the batch script, and can be obtained by typing the following within the python window in either ArcMap or ArcPro;

	import sys
	print (sys.version)
	
The python version info should then be updated in the batch script where you find the following text, noting the version may be different; python=3.6.8 


# Installation
The following instructions assume that there are no instances of Python installed other than the ones bundled with ArcGIS. Please uninstall PythonXY or any other Python distributions you may have installed before commencing the Anaconda installation.

Please perform the required installation(s) for your version(s) of ArcGIS, selecting the "Just Me" option to install in user-space (i.e. without requiring administrative privileges), and accept all other default options except the "Set as default Python 2/3". N.B: DO NOT CHECK THE "Set as default Python 2/3" OPTION - CHECKING IT WILL CAUSE THE ARCGIS INTEGRATION TO FAIL.

ArcMap 10.5 requires a user-space installation of the 32-bit version of Anaconda Python 2 (https://repo.anaconda.com/archive/Anaconda2-5.2.0-Windows-x86.exe). N.B: DO NOT INSTALL THE 64-BIT VERSION OF PYTHON 2 UNLESS ABSOLUTELY NECESSARY, AND THEN ONLY AFTER READING THE NOTE BELOW.

ArcGIS Pro  requires a user-space installation of the 64-bit version of Anaconda Python 3 (https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe). N.B: DO NOT INSTALL THE 32-BIT VERSION OF PYTHON 3 UNLESS ABSOLUTELY NECESSARY, AND THEN ONLY AFTER READING THE NOTE BELOW.

Note that you will need to separate the 32-bit and 64-bit versions of either Python 2 or 3 if you require both on your system, since both installers for a given version of Python will attempt to write to the one directory. Recommended practice in this case would be to add a "_32" or "_64" suffix to each default istallation directory in order to explicitly identify which is which. You will also need to adjust the CONDA_CONFIG section of usercustomize.py to be able to find the "Anaconda2_32" directory for Python 2, since the default settings will look for the default "Anaconda2" directory.

After you have installed the required version(s) of Anaconda, download or clone this repo (https://github.com/GeoscienceAustralia/arcgis_conda_integration.git) to a known directory (e.g. C:\Temp\arcgis_conda_integration), then open the "Anaconda Prompt" shortcut under the relevant version of Anaconda. At the resultant command line, change directory to the one containing these files, and then run the relevant batch file for the Anaconda version, i.e. prepare_anaconda2.bat for Anaconda2, or prepare_anaconda3.bat for Anaconda3. Each batch file will:
- update the base environment of Anaconda
- install some generally useful packages not included in the initial Anaconda installation to the base environment
- create a virtual environment with specific package versions for ArcGIS compatibility
- copy the usercustomize.py script to C:\Users\%username%\AppData\Roaming\Python\Python36\site-packages

Note that if you are prompted for administrative access, you can either accept this if you have access to an administrator account, or just click "Cancel" - this is caused by some packages trying (erroneously) to write to the shared startup menu, and will not affect the actual installations or updates. Once the script has completed, you should be able to start the Anaconda Python, and enter "import arcpy" without error. We may include a work-around to create the missing user start-menu icons at a later date.

If you have any issues updating Conda due to proxy issues, you may need to explicitly configure your proxy in the .condarc file in your user directory (e.g. C:\Users\%USERNAME\.condarc). 

If you do not have a .condarc file in your user directory you can create one by entering the command "conda config --write-default" using the Anaconda Prompt.

For GA, you may need to make sure the following section appears in that file:

	proxy_servers:
	    http: http://proxy.ga.gov.au:8080
	    https: https://proxy.ga.gov.au:8080
Please see https://conda.io/docs/user-guide/configuration/use-condarc.html#config-proxy for further information. 

To use the ArcGIS-compatible virtual environment, you can use the versions of Spyder and/or Jupyter installed in the virtual environment by using the shortcuts in the start menu. Alternatively, you can start the "Anaconda Prompt" for the relevant Python, and then type "activate arc105_32bit" for ArcMap 105 / Python 2.7, or "activate arcgispro-py3" for ArcGIS Pro / Python 3.6. You can then start Python, Jupyter or anything else in the virtual environment from that command prompt.

# Optional - Creating your own Conda Virtual Environments / Recovery
Should you wish to test different versions of packages, it is possible to clone the virtual environment as follows:

For ArcMap 105 / Python 2.7:

	conda create --name myclone --clone arc105_32bit 
For ArcGIS Pro / Python 3.6:

	conda create --name myclone --clone arcgispro-py3  
Note that if you wish to use the libraries in your cloned environment from within ArcGIS, you will need to manually edit the 'default_environment' value in the CONDA_CONFIG variable in the file C:\Users\%username%\AppData\Roaming\Python\Python<27|36>\site-packages\usercustomize.py. This is because the usercustomize script can only integrate a single virtual environment.

Should you corrupt a Conda virtual environment, it is possible to delete it and recreate it from a known starting point. Please refer to https://conda.io/docs/user-guide/tasks/manage-environments.html for more information. In a worst-case scenario, it is also possible to manually delete all files and shortcuts created by the user-space installation, and start the installation procedure completely afresh.

There is also a PDF Conda Cheat Sheet at https://conda.io/docs/_downloads/conda-cheatsheet.pdf which might be of use.

# Contacts and Acknowledgments
To provide feedback or obtain further information on this repo, please contact the eGIS team at Geoscience Australia (egis@ga.gov.au).

The version of usercustomize.py in this repo was functionally based on an original script written by Curtis Price of USGS (cprice@usgs.gov).
This usercustomize.py script was written by Alex Ip of Geoscience Australia, based on an augmented version of Curtis Price's script by Duncan Moore, also of GA.
