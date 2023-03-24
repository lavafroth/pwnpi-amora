import glob
from subprocess import PIPE, Popen
from os import listdir, makedirs
from os.path import join, splitext
from shutil import copytree, copy
from errno import ENOTDIR
SRC = 'src'
DST = 'build'


def cp(src, dst):
    try:
        copytree(src, dst)
    except OSError as exc:
        if exc.errno == ENOTDIR:
            copy(src, dst)
        else:
            raise


def to_compile(s: str):
    name, ext = splitext(s)
    if name not in ("code", "boot") and ext == ".py":
        return name
    return None


makedirs(DST, exist_ok=True)
mpy_cross_bin = join(".", glob.glob("mpy-cross.static*")[0])

for entry in listdir(SRC):
    src_path = join(SRC, entry)
    if name := to_compile(entry):
        Popen([
            mpy_cross_bin,
            "-o",
            join(DST, f'{name}.mpy'),
            src_path,
        ],
            stdout=PIPE,
        ).communicate()
    else:
        dst_path = join(DST, entry)
        cp(src_path, dst_path)
