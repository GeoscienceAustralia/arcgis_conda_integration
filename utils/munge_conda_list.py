#!/usr/bin/env python
# coding: utf-8
'''
Quick and dirty utility to take the output of a "conda list" command and turn
it into forms that can be cut-and-pasted into ArcGIS integration setup scripts.
'''
import re

conda_list_file_path = 'C:\\W10Dev\\Temp\\arcgis_conda_integration\\argispro-py3_conda_list.txt'
excluded_packages = ['arcgis', 
                     'arcgispro',
                     'icc_rt',
                     'pypdf2',
                     'pywin32-ctypes', 
                     ]

requirements=[]
with open(conda_list_file_path) as conda_list_file:
    for line in conda_list_file:
        line = re.sub('\s+', ' ', line.strip())
        
        if line[0] == '#':
            continue
            
        values = line.split(' ')
        
        # if values[-1] == 'esri':
        #     continue
        
        if values[0] in excluded_packages:
            continue
            
        requirements.append('{}={}'.format(*values[0:2]))
        
    conda_list_file.close()
        
print('conda create --yes --name %environment_name% ' + ' '.join(requirements) + ' jupyter spyder')
print()
print('\n'.join([requirement.replace('=', '==') for requirement in requirements]))
