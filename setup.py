import sys
from cx_Freeze import setup, Executable


include_files = []
include_files += ["icons/"]
include_files += ["config_template.json"]

build_exe_options = {
    "packages": ["PySide6.QtWidgets", "PySide6.QtCore", "PySide6.QtGui", "rich", "qdarktheme"], 
    "excludes": ["tkinter"],
    "include_files": include_files,
    "include_msvcr": True
}

program_name = "Godot Project Manager alternative"

base = None
exe_postfix = None
if sys.platform == "win32":
    base = "Win32GUI"
    exe_postfix = ".exe"

setup(
    name = program_name,
    version = "1.0.0",
    description= "",
    options = {
        "build_exe": build_exe_options,
    },
    executables = [
        Executable("main.py", base=base, targetName=f"GBPM{exe_postfix if exe_postfix else ''}")
    ],
)