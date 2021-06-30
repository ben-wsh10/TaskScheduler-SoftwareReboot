import sys
from distutils.core import setup
import py2exe

# python to exe script
# 1. Open cmd prompt in this file directory
# 2. pip install py2exe
# 3. type in the following cmd to convert script : python setup.py py2exe
# 4. executable is found in this file directory
# 5. delete all files except for executable file

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    # Input absolute path below
    console = [{'script': "D:\Coding\Python\TS&SR\BackEnd\Main.py"}],
    zipfile = None,
)