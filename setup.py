import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["textual", "rich"],
    "excludes": [],
    "include_files": ["data/"],
}

# Base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Console"

setup(
    name="StudentManager",
    version="1.0",
    description="University Student Manager TUI Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base=base, target_name="StudentManager.exe")],
)