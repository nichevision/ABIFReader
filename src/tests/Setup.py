from distutils.core import setup
import py2exe

setup(name="modHIDFile",
      console=["modHIDFile.py"],
      package_dir = { 'ABIF' : '../ABIF'},
      py_modules=["ABIF",],)