#!/usr/bin/env python3
"""
Builder script to compile .py files to .mpy bytecode using mpy-cross
"""

import glob
from errno import ENOTDIR
from os import listdir, makedirs
from os.path import join, splitext
from shutil import copy, copytree, rmtree
from subprocess import PIPE, Popen

SRC = "src"
DST = "build"


def recursive_copy(src: str, dst: str):
    """
    Copy a file or directory from src to dst.

    Parameters:
        src (str): The path of the source file or directory.
        dst (str): The path of the destination file or directory.

    Returns:
        None
    """
    try:
        copytree(src, dst)
    except OSError as exc:
        if exc.errno == ENOTDIR:
            copy(src, dst)
        else:
            raise


def to_compile(name: str) -> str:
    """
    Check if a given file is a Python source file that needs to be compiled.

    Parameters:
        name (str): The name of the file.

    Returns:
        str: The name of the file without the extension if it need compilation,
        otherwise None.
    """
    base, ext = splitext(name)
    if base not in ("code", "boot") and ext == ".py":
        return base
    return None


def main():
    """
    Use mpy-cross to compile .py files to .mpy bytecode
    """

    # Remove the build directory if it exists, then create it again
    rmtree(DST, ignore_errors=True)
    makedirs(DST, exist_ok=True)
    makedirs(join(DST, "lib"), exist_ok=True)

    # Find the path of the mpy-cross binary
    mpy_cross_bin = join(".", glob.glob("mpy-cross.static*")[0])

    # Process each entry in the source directory
    for entry in listdir(SRC):
        src_path = join(SRC, entry)
        # If the entry is a Python source file that needs to be compiled
        if name := to_compile(entry):
            # Compile the file using mpy-cross
            with Popen(
                [mpy_cross_bin, "-o",
                    join(DST, "lib", f"{name}.mpy"), src_path],
                stdout=PIPE,
            ) as process:
                process.communicate()
        else:
            # Copy the file or directory to the build directory
            dst_path = join(DST, entry)
            recursive_copy(src_path, dst_path)


if __name__ == "__main__":
    main()
