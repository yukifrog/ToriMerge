$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
pip install . pyinstaller
pyinstaller -y --collect-all pandas --collect-all openpyxl torimerge-cli.spec
pyinstaller -y --collect-all pandas --collect-all openpyxl torimerge-gui.spec
