#!/usr/bin/env python

#===============================================================================
#    Copyright 2017 Geoscience Australia
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#===============================================================================
'''
Created on 16/07/2018

@author: Alex Ip

Startup script to link Anaconda python environment with ArcGIS
This script will modify the search path by appending ArcGIS libraries to Anaconda ones for
Anaconda Python, or the Anaconda libraries to the ArcGIS ones for ArcGIS Python
 
Functionality based on original usercustomize.py script by from Curtis Price, cprice@usgs.gov
This script was re-written Alex Ip based on an augmented version by Duncan Moore.
It is intended to allow users to use ArcPy with multiple, arbitrary Conda environments
Note that only the 32-bit ArcMap 10.5 and 64-bit ArcGIS Pro integrations have been actively tested.
'''
import os
import sys
import struct
import logging
import re
import pkg_resources
from pprint import pformat
try:
    import winreg # Python 3
except:
    import _winreg as winreg # Python 2

#===========================================================================
# Edit these values as required

# change to false after testing done
DEBUG = False

# Set this to handle possible version incompatibilities
PACKAGE_CHECK_ACTION = 'warn' # Can be 'ignore', 'warn' or 'abort'

# Root directory of ArcGIS Python installation
ARCGIS_DESKTOP_PYTHON_ROOT = 'C:\\Python27' 

# Default Conda prefixes (absolute or relative to default envs dir) for Python version and bits
# N.B: Can also set CONDA_PREFIX environment variable outside conda
CONDA_DEFAULT_PREFIXES = {(2, 32): 'C:\\anaconda2_32bit\\envs\\_arc105_32bit',
                          (3, 64): 'arcgispro-py3'
                          }

# Define optional package version constraints for each Python version
PACKAGE_VERSION_CONSTRAINTS = {(2, 32): {'python': '2.7.12',
                                         'numpy': '1.11.2',
                                         'matplotlib': '1.5.3',
                                         'scipy': '0.17.0'
                                         },
                               (3, 64): {'python': '3.6.6',
                                         'numpy': '1.13.3',
                                         'matplotlib': '2.0.2',
                                         'scipy': '0.19.1'
                                         }
                               }
#===========================================================================

logger = logging.getLogger(__name__) # Get __main__ logger
# Set initial logging level for this module
if DEBUG:
    logger.setLevel(logging.DEBUG) 
else:
    logger.setLevel(logging.INFO)
    
if not logger.handlers:
    # Set handler for root logger to standard output
    console_handler = logging.StreamHandler(sys.stdout)
    #console_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
logger.debug('os.environ: {}'.format(pformat(dict(os.environ))))

def usercustomise():
    '''
    Function to customise Python paths for ArcGIS/Conda integration
    '''
    def get_arcgis_pro_path():
        '''
        Function to find Pro Path (in registry)
        '''
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\ESRI\ArcGISPro",
                             0,
                             winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
            return winreg.QueryValueEx(key, "InstallDir")[0]
    
    
    def set_sys_paths(pth_file_path, is_arcgis_pro=False):
        """
        Function to unpack .pth file to list of paths
        """
        logger.debug('pth_file_path: {}'.format(pth_file_path))
        
        if not os.path.isfile(pth_file_path):
            raise BaseException('ArcGIS .pth file {} does not exist'.format(pth_file_path))
        
        if is_arcgis_pro: # ArcGIS Pro - need to "execfile" .pth file as a Python file
            try:
                sys.path.append(os.path.dirname(pth_file_path))

                exec(compile(open(pth_file_path, "rb").read(), pth_file_path, 'exec'), globals(), locals())
                
                #===============================================================
                # # N.B: This does not seem to be required - it results in a duplicate (A.I.)
                # # additional fix: add Pro's bin folder to system path
                # # https://geonet.esri.com/thread/191758-how-to-run-python-with-the-arcgis-pro-14-from-outside?start=0&tstart=0#comment-677397
                # os.environ["PATH"] = "{};{}".format(os.path.join(arcgis_install_dir, "bin"),
                #                                     os.environ["PATH"])
                #===============================================================
            
            except BaseException as e:
                raise BaseException("could not execfile {}: {}".format(pth_file_path, e.message))
        else: # ArcGIS Desktop - .pth file is a list of directories
            try:
                sp = os.path.dirname(pth_file_path)
                sys.path += [sp] + [p.strip() for p in open(pth_file_path, "r")]
            except BaseException as e:
                logger.error("could not read and append paths from {}: {}".format(pth_file_path, e.message))
            
    def check_package_versions(arcgis_name='ArcGIS', action='warn'):
        '''
        Function to check if packages aren't as expected for Conda Python version to 
        match corresponding ArcGIS Python packages
        '''
        assert action in ['ignore', 'warn', 'abort'], 'Invalid action: "{}"'.format(action)
        
        package_version_constraints = PACKAGE_VERSION_CONSTRAINTS.get((python_major_version, python_bits))
        if package_version_constraints:
            for package_name, required_version in package_version_constraints.items():
                actual_version = ('.'.join([str(version) for version in sys.version_info[0:3]]) 
                                  if package_name == 'python'
                                  else pkg_resources.get_distribution(package_name).version
                                  )
                if actual_version != required_version:
                    message = '{} must be version {} for {}. Found {}'.format(package_name, 
                                                                              required_version, 
                                                                              arcgis_name,
                                                                              actual_version)
                    if action == 'warn':
                        logger.warning('WARNING: {}'.format(message))
                    elif action == 'abort':
                        raise BaseException(message)
                    else: # action == 'ignore'
                        logger.debug('DEBUG: {}'.format(message))
    
    
    def get_conda_default_prefix(arcgis_python_dir):
        '''
        Function to return conda_default_prefix for non-ArcGIS invocations
        '''
        conda_default_prefix = (os.environ.get('CONDA_DEFAULT_PREFIX') # N.B: This is NOT as standard Conda variable
                                or CONDA_DEFAULT_PREFIXES.get((python_major_version, python_bits)) 
                                )
        if conda_default_prefix: 
            if not '\\' in conda_default_prefix: # Relative to envs in ArcGIS Pro Conda installation - make absolute
                conda_default_prefix = os.path.join(arcgis_python_dir, 'envs', conda_default_prefix)
                
        return conda_default_prefix
    #===========================================================================
    # # Sample Conda environment variable values
    #  'AGSDESKTOPJAVA': 'C:\\Program Files (x86)\\ArcGIS\\Desktop10.5\\',
    #  'CONDA_DEFAULT_ENV': '_arc105_32bit',
    #  'CONDA_EXE': 'C:\\anaconda2_32bit\\Scripts\\conda.exe',
    #  'CONDA_PREFIX': 'C:\\anaconda2_32bit\\envs\\_arc105_32bit',
    #  'CONDA_PREFIX_1': 'C:\\anaconda2_32bit',
    #  'CONDA_PROMPT_MODIFIER': '(_arc105_32bit) ',
    #  'CONDA_PYTHON_EXE': 'C:\\anaconda2_32bit\\python.exe',
    #===========================================================================

    # Check version of Python
    python_major_version = sys.version_info[0] # 2 or 3
    logger.debug('python_major_version: {}'.format(python_major_version))
    
    python_bits = struct.calcsize("P") * 8
    logger.debug('python_bits: {}'.format(python_bits))
    
    CONDA_PREFIX = os.environ.get('CONDA_PREFIX')
    
    if python_major_version == 2: # Python 2.X - assume ArcGIS Desktop
        arcgis_name = 'ArcGIS Desktop'
        
        arcgis_install_dir = os.environ["AGSDESKTOPJAVA"]
        try:
            arcgis_version = re.search('.*(\d\d\.\d)(\\\\)?', arcgis_install_dir).group(1) # e.g. '10.5'
        except:
            raise BaseException('Unable to determine version for {} installation at {}'.format(arcgis_name,
                                                                                               arcgis_install_dir))
        
        if python_bits == 32:
            if not os.path.isfile(os.path.join(arcgis_install_dir, "bin", "ArcMap.exe")):
                raise BaseException('No 32-bit {} executable found'.format(arcgis_name))
            arcgis_python_dir = os.path.join(ARCGIS_DESKTOP_PYTHON_ROOT, 'ArcGIS{}'.format(arcgis_version))
            pth_file_path = os.path.join(arcgis_python_dir, "Lib\\site-packages\\Desktop{}.pth".format(arcgis_version))
        elif python_bits == 64:
            if not os.path.isfile(os.path.join(arcgis_install_dir, "bin64", "RuntimeLocalServer.exe")):
                BaseException('No 64-bit {} executable found'.format(arcgis_name))
            arcgis_python_dir = os.path.join(ARCGIS_DESKTOP_PYTHON_ROOT, 'ArcGISx64{}'.format(arcgis_version))
            pth_file_path = os.path.join(arcgis_python_dir, "Lib\\site-packages\\DTBGGP64.pth")
        else:
            raise BaseException('Invalid number of bits for Python: {}'.format(python_bits)) 
        
        is_arcgis_python = sys.executable.lower().startswith(arcgis_python_dir.lower())
        is_arcgis_pro = False # ArcGIS Desktop .pth file is a list of paths which must NOT be executed
        
        conda_default_prefix = get_conda_default_prefix(arcgis_python_dir)
           
    elif python_major_version == 3: # Python 3.X - assume ArcGIS Pro
        arcgis_name = 'ArcGIS Pro'
        
        if python_bits != 64:
            raise BaseException('{} does not support 32-bit Python'.format(arcgis_name))
        
        if not CONDA_PREFIX:
            raise BaseException('{} requires a Conda invocation of Python'.format(arcgis_name))
        
        try:
            arcgis_install_dir = get_arcgis_pro_path()
        except:
            raise BaseException('Unable to determine installation directory for {}'.format(arcgis_name))
        
        if not os.path.isfile(os.path.join(arcgis_install_dir, "bin\\ArcGISPro.exe")):
            raise BaseException('No {} executable found'.format(arcgis_name))
        
        arcgis_python_dir = os.path.join(arcgis_install_dir, 'bin\\Python') 
        
        is_arcgis_python = sys.executable.lower().startswith(arcgis_python_dir.lower())
        is_arcgis_pro = True # ArcGIS Pro .pth file is a Python file which must be executed
        
        conda_default_prefix = get_conda_default_prefix(arcgis_python_dir)
                
        if is_arcgis_python: # ArcGIS invocation - use actual Conda prefix
            pth_file_path = os.path.join(CONDA_PREFIX, "Lib\\site-packages\\ArcGISPro.pth")
        else: # Non-ArcGIS invocation - use default ArcGIS Conda prefix
            pth_file_path = os.path.join(conda_default_prefix, "Lib\\site-packages\\ArcGISPro.pth")
    else:
        raise BaseException('Python {} is unsupported'.format(python_major_version))
      
    logger.debug('arcgis_python_dir: {}'.format(arcgis_python_dir))
    if not os.path.isdir(arcgis_python_dir):
        raise BaseException('{} Python directory {} does not exist'.format(arcgis_name,
                                                                           arcgis_python_dir))
    
    # Initialisation completed - now set search paths
    
    # Non-ArcGIS Conda invocation - append ArcGIS libs
    if CONDA_PREFIX and not is_arcgis_python: 
        set_sys_paths(pth_file_path, is_arcgis_pro)
        check_package_versions(arcgis_name, PACKAGE_CHECK_ACTION) # Only check Conda invocations. ArcGIS ones should be OK
        
        logger.info('Conda Python customised with libs from {}'.format(arcgis_name))
        
    # ArcGIS (Desktop) non-Conda invocation - append default Conda lib
    elif is_arcgis_python and not CONDA_PREFIX: 
        conda_site_packages_dir = os.path.join(conda_default_prefix, "Lib\\site-packages")
        logger.debug('conda_site_packages_dir: {}'.format(conda_site_packages_dir))
        if not os.path.isdir(conda_site_packages_dir):
            raise BaseException('Directory {} does not exist.'.format(conda_site_packages_dir))
        sys.path.append(conda_site_packages_dir)

        logger.info('{} Python customised with libs from Conda environment {}'.format(arcgis_name,
                                                                                  conda_default_prefix))

    else: # ArcGIS (Pro) Conda invocation or non-ArcGIS non-Conda invocation - do nothing
        logger.debug('Python not customised with libs from ArcGIS or Conda')            
        
    logger.debug("sys.path: {}".format(';\n\t'.join(sys.path)))
    logger.debug('os.environ["PATH"]: {}'.format(';\n\t'.join([path_dir.strip() 
                                                             for path_dir in os.environ["PATH"].split(';')
                                                             if path_dir.strip()
                                                             ]
                                                             )))


# This script is not required for ArcGIS python invocations - only Conda invocations
try:
    usercustomise()
except BaseException as e:
    logger.debug('ArcPy/Conda integration not set up: {}'.format(e.message if hasattr(e, 'message') else e))
