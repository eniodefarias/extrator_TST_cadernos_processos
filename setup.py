from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("dejt_001_extrator_TST.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Nome Executavel",
    options = options,
    version = "1.0",
    description = 'Descricao do seu arquivo',
    executables = executables
)