# pip install cx_freeze
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame", "pyttsx3", "pyttsx3.drivers", "pyttsx3.drivers.sapi5"],
    "include_files": ["Bases", "recursos", "log.dat"]
}

setup(
    name="Void Knight",
    version="1.0",
    description="Jogo Void Knight",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", target_name="Void Knight.exe")]
)

# python setup.py build
# python setup.py bdist_msi