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
 
Functionality based on original usercustomize.py script by Curtis Price of USGS (cprice@usgs.gov)
This script was re-written by Alex Ip of Geoscience Australia, based on an augmented version by 
Duncan Moore, also of GA.
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

# Root directory of ArcGIS Desktop Python installation
# ArcGIS Pro Python root will be found relative to registry entry
ARCGIS_DESKTOP_PYTHON_ROOT = 'C:\\Python27' 

# Anaconda configuration by Python version and bit width
CONDA_CONFIG = {(2, 32): {'installation_root': 'C:\\W10Dev\\Continuum\\Anaconda2',
                          'default_environment': 'arc105_32bit', # Default Conda environment to add to ArcGIS Python
                          'required_package_versions': {},
                          'bin_dirs': ['',
                                       'Library\\usr\\bin',
                                       'Library\\bin',
                                       'Scripts',
                                       'bin',
                                       ],
                          },
                (3, 64): {'installation_root': 'C:\\W10Dev\\Continuum\\Anaconda3',
                          'default_environment': 'arcgispro-py3', # Default Conda environment to add to ArcGIS Python
                          'required_package_versions': {},
                          'bin_dirs': ['',
                                       'Library\\mingw-w64\\bin',
                                       'Library\\usr\\bin',
                                       'Library\\bin',
                                       'Scripts',
                                       'bin',
                                       ],
                          }
                }

# Read pinned file to determine what versions should be installed
for python_version, python_config in CONDA_CONFIG.items():
    pinned_file_path = '{}\\envs\\{}\\conda-meta\\pinned'.format(python_config['installation_root'],
                                                                 python_config['default_environment'])
    if not os.path.isfile(pinned_file_path):
        continue
    
    with open(pinned_file_path) as pinned_file:
        for line in pinned_file:
            line = re.sub('\s+', ' ', line.strip())
        
            if line[0] == '#':
                continue
            
            values = line.split('==')
            python_config['required_package_versions'][values[0]] = values[1]

        pinned_file.close()

    

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
        
        required_package_versions = CONDA_CONFIG[(python_major_version, python_bits)]['required_package_versions']
        if required_package_versions:
            for package_name, required_version in required_package_versions.items():
                try:
                    actual_version = ('.'.join([str(version) for version in sys.version_info[0:3]]) 
                                      if package_name == 'python'
                                      else pkg_resources.get_distribution(package_name).version
                                      )
                    if actual_version != required_version:
                        message = '{} should be version {} for {}. Found {}'.format(package_name, 
                                                                                  required_version, 
                                                                                  arcgis_name,
                                                                                  actual_version)
                        if action == 'warn':
                            logger.warning('WARNING: {}'.format(message))
                        elif action == 'abort':
                            raise BaseException(message)
                        else: # action == 'ignore'
                            logger.debug('DEBUG: {}'.format(message))
                except Exception as e:
                    logger.debug('Unable to determine version for {}: {}'.format(package_name, e))
    
    def get_conda_default_prefix(python_major_version, python_bits, username):
        '''
        Function to return conda_default_prefix for non-ArcGIS invocations
        '''
        conda_default_prefix = (os.environ.get('CONDA_DEFAULT_PREFIX') # N.B: This is NOT a standard Conda variable - set by ESRI
                                # Non-ArcGIS 
                                or os.path.join(CONDA_CONFIG[(python_major_version, python_bits)]['installation_root'], 
                                                'envs', 
                                                CONDA_CONFIG[(python_major_version, python_bits)]['default_environment'])
                                )

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
    conda_default_env = os.environ.get("CONDA_DEFAULT_ENV")
    if conda_default_env == 'base':
        logger.debug('Conda base environment not modified for ArcGIS')
        sys.exit()
        
    username = os.environ.get('USERNAME')
    
    # Check version of Python
    python_major_version = sys.version_info[0] # 2 or 3
    logger.debug('python_major_version: {}'.format(python_major_version))
    
    python_bits = struct.calcsize("P") * 8
    logger.debug('python_bits: {}'.format(python_bits))
    
    CONDA_PREFIX = os.environ.get('CONDA_PREFIX')
    
    if python_major_version == 2: # Python 2.X - assume ArcGIS Desktop
        arcgis_name = 'ArcGIS Desktop 10.5'
        
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
        
        conda_default_prefix = get_conda_default_prefix(python_major_version, python_bits, username)
           
    elif python_major_version == 3: # Python 3.X - assume ArcGIS Pro
        arcgis_name = 'ArcGIS Pro'
        
        if python_bits != 64:
            raise BaseException('{} does not support 32-bit Python'.format(arcgis_name))
        
        if not CONDA_PREFIX:
            raise BaseException('{} requires a Conda invocation of Python'.format(arcgis_name))
        
        try:
            arcgis_install_dir = get_arcgis_pro_path()
            logger.debug('arcgis_install_dir: {}'.format(arcgis_install_dir))
        except:
            raise BaseException('Unable to determine installation directory for {}'.format(arcgis_name))
        
        if not os.path.isfile(os.path.join(arcgis_install_dir, "bin\\ArcGISPro.exe")):
            raise BaseException('No {} executable found'.format(arcgis_name))
        
        arcgis_python_dir = os.path.join(arcgis_install_dir, 'bin\\Python') 
        
        is_arcgis_python = sys.executable.lower().startswith(arcgis_python_dir.lower())
        is_arcgis_pro = True # ArcGIS Pro .pth file is a Python file which must be executed
        logger.debug('is_arcgis_python={}, is_arcgis_pro={}'.format(is_arcgis_python, is_arcgis_pro))
        
        if is_arcgis_python: # ArcGIS invocation - use actual Conda prefix
            conda_default_prefix = os.path.join(CONDA_CONFIG[(python_major_version, python_bits)]['installation_root'],
                                                'envs',
                                                CONDA_CONFIG[(python_major_version, python_bits)]['default_environment']
                                                )                
            pth_file_path = os.path.join(CONDA_PREFIX, "Lib\\site-packages\\ArcGISPro.pth")
        else: # Non-ArcGIS invocation - use default ArcGIS Conda prefix
            conda_default_prefix = os.path.join(arcgis_python_dir,
                                                'envs',
                                                CONDA_CONFIG[(python_major_version, python_bits)]['default_environment']
                                                )                
            pth_file_path = os.path.join(conda_default_prefix, "Lib\\site-packages\\ArcGISPro.pth")
    else:
        raise BaseException('Python {} is unsupported'.format(python_major_version))
      
    logger.debug('arcgis_python_dir: {}'.format(arcgis_python_dir))
    if not os.path.isdir(arcgis_python_dir):
        raise BaseException('{} Python directory {} does not exist'.format(arcgis_name,
                                                                           arcgis_python_dir))
    
    # Create cleaned path list
    path_list = []
    for path_dir in [path_dir.strip() 
                 for path_dir in os.environ["PATH"].split(';')
                 if path_dir.strip()
                 ]:
        if ((path_dir not in path_list)
            and os.path.isdir(path_dir)
            and ((python_major_version == 2) or ('Python27' not in path_dir))): # Strip Python27 directory from path if using Python 3
            path_list.append(path_dir)
                                      
    # Initialisation completed - now set search paths
    
    # Non-ArcGIS Conda Python invocation - append ArcGIS libs
    if CONDA_PREFIX and not is_arcgis_python: 
        set_sys_paths(pth_file_path, is_arcgis_pro)
        
        # Append binary directories for ArcGIS Conda installation
        path_list.append(os.path.join(arcgis_install_dir, 'bin'))
                         
        for path_dir in [os.path.join(arcgis_python_dir, 
                                      'envs', 
                                      CONDA_CONFIG[(python_major_version, python_bits)]['default_environment'],
                                      bin_dir
                                      )
                         for bin_dir in CONDA_CONFIG[(python_major_version, python_bits)]['bin_dirs']
                         ]:

            if (path_dir not in path_list) and os.path.isdir(path_dir):
                path_list.append(path_dir)

        os.environ["PATH"] = ';'.join(path_list)

        check_package_versions(arcgis_name, PACKAGE_CHECK_ACTION) # Only check Conda invocations. ArcGIS ones should be OK
        
        logger.info('Conda Python customised with libs from {}'.format(arcgis_name))
    # ArcGIS Python invocation - append default Conda environment libs
    elif is_arcgis_python:
        conda_site_packages_dir = os.path.join(CONDA_CONFIG[(python_major_version, python_bits)]['installation_root'], 
                                               'envs', 
                                               CONDA_CONFIG[(python_major_version, python_bits)]['default_environment'],
                                               'Lib',
                                               'site-packages'
                                               )
        logger.debug('conda_site_packages_dir: {}'.format(conda_site_packages_dir))
        if not os.path.isdir(conda_site_packages_dir):
            raise BaseException('Directory {} does not exist.'.format(conda_site_packages_dir))
        sys.path.append(conda_site_packages_dir)

        # Append binary search paths for non-ArcGIS Conda installation
        for path_dir in [os.path.join(CONDA_CONFIG[(python_major_version, python_bits)]['installation_root'], 
                                      'envs', 
                                      CONDA_CONFIG[(python_major_version, python_bits)]['default_environment'],
                                      bin_dir
                                      )
                         for bin_dir in CONDA_CONFIG[(python_major_version, python_bits)]['bin_dirs']
                         ]:

            if (path_dir not in path_list) and os.path.isdir(path_dir):
                path_list.append(path_dir)

        os.environ["PATH"] = ';'.join(path_list)

        logger.info('{} Python customised with libs from Conda environment {}'.format(arcgis_name,
                                                                                      conda_site_packages_dir))

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
