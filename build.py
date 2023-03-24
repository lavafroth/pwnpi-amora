import glob
from subprocess import PIPE, Popen
from os import listdir, makedirs
from os.path import join, splitext, isfile
from shutil import copytree, copy
SRC = 'src'
DST = 'build'


def lib_files(s: str):
    name, ext = splitext(s)
    if name not in ("code", "boot") and ext == ".py" and isfile(s):
        return name
    return None


makedirs(DST, exist_ok=True)

for entry in listdir(SRC):
    src_path = join(SRC, entry)
    if name := lib_files(entry):
        Popen([
            join(".", glob.glob("mpy-cross.static*")[0]),
            src_path, "-o",
            join(DST, f'{name}.mpy')
        ],
            stdout=PIPE
        ).communicate()
    else:
        dst_path = join(DST, entry)
        if isfile(join(SRC, entry)):
            copy(src_path, dst_path)
        else:
            copytree(src_path, dst_path)
