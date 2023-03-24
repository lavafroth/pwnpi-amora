import glob
from subprocess import PIPE, Popen
from os import listdir, makedirs
from os.path import join, splitext, isfile
from shutil import copytree, copy
SRC = 'src'
OUT = 'build'


def lib_files(s: str):
    name, ext = splitext(s)
    if name not in ("code", "boot") and ext == ".py" and isfile(s):
        return name
    return None


makedirs(OUT, exist_ok=True)

for entry in listdir(SRC):
    if name := lib_files(entry):
        Popen([
            join(".", glob.glob("mpy-cross.static*")[0]),
            join(SRC, entry),
            "-o",
            join(OUT, f'{name}.mpy')
        ],
            stdout=PIPE
        ).communicate()
    elif isfile(join(SRC, entry)):
        copy(join(SRC, entry),
             join(OUT, entry))
    else:
        copytree(join(SRC, entry),
                 join(OUT, entry))
