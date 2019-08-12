#!/usr/bin/env python
# coding: utf-8
'''
Quick and dirty utility to dump PATH environment variable and system path.
'''

import sys, os
print('\nos.environ[\'PATH\'] contents:')
for dir in os.environ['PATH'].split(';'):
    print(dir)

print('\nsys.path contents:')
for dir in sys.path:
    print(dir)

