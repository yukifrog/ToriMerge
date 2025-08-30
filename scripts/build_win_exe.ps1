$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
pip install . pyinstaller
pyinstaller -y --name torimerge --console -F -i NONE -s -w src/torimerge/cli.py
pyinstaller -y --name torimerge-gui --windowed -F -i NONE -s src/torimerge/gui.py
