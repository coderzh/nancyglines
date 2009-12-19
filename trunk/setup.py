from distutils.core import setup
import py2exe

setup(windows = [{"script":"glines.py", "icon_resources": [(1, "glines.ico")]}],
      data_files=["glines.png"])