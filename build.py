import nicegui
from pathlib import Path
import subprocess
static_dir = Path(nicegui.__file__).parent

script = f'pyinstaller --onefile gui.py --add-data="{static_dir};nicegui"'
subprocess.call(script, shell=True)