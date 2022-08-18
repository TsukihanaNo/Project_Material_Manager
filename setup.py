import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                    "packages": ["os","PySide6"],
                    "excludes": ["tkinter"],
                    "optimize": True,
                    "include_files":['icons/','templates/'],
                    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Project Material Manager",
        version = "1.0",
        description = "Project Material Manager",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Manager.py",base = base)])