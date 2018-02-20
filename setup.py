
import scipy
import os
import sys
import cx_Freeze
from distutils.core import setup
import matplotlib


includes = ['numpy.core._methods','re','numpy.matlib','matplotlib.backends.backend_tkagg',
'FileDialog','lxml._elementpath']


includefiles_list=[(matplotlib.get_data_path(), "mpl-data")]

scipy_path = os.path.dirname(scipy.__file__)
includefiles_list.append(scipy_path)


packages = ["Tkinter", "tkFileDialog"]

excludes= ["collections.abc"]



build_exe_options = {"includes" : includes,'include_files':includefiles_list,'packages':packages,"excludes": excludes}
   
exe = cx_Freeze.Executable(
    script="main2.py",
    base="Win32GUI",
    )

cx_Freeze.setup(
    name = "wxSampleApp",
    version = "0.1",
    description = "An example wxPython script",
    options = { "build_exe" : build_exe_options },
    executables = [exe]

    )





