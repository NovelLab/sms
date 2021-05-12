"""Utility module for file paths."""

# Official Libraries
import glob
import os


__all__ = (
        'add_extention',
        'basename_of',
        'filenames_with_number',
        'get_filepaths_in',
        'is_exists_path',
        'joinpath',
        'make_dir',
        'new_filename_by_input',
        )


# Main
def add_extention(fname: str, ext: str) -> str:
    assert isinstance(fname, str)
    assert isinstance(ext, str)

    return f"{fname}.{ext}"


def basename_of(filepath: str, is_only_name: bool = True) -> str:
    assert isinstance(filepath, str)

    fname = os.path.basename(filepath)

    if is_only_name:
        return os.path.splitext(fname)[0]
    else:
        return fname


def filenames_with_number(fnames: list, first_num: int = 1) -> list:
    assert isinstance(fnames, list)
    assert isinstance(first_num, int)

    tmp = []
    idx = first_num

    for fname in fnames:
        assert isinstance(fname, str)
        tmp.append(f"{idx}: {fname}")
        idx += 1
    return tmp


def get_filepaths_in(dirname: str, ext: str, is_recursive: bool = False) -> list:
    assert isinstance(dirname, str)
    assert isinstance(ext, str)
    assert isinstance(is_recursive, bool)

    return glob.glob(f"{dirname}/*.{ext}", recursive=is_recursive)


def is_exists_path(path: str) -> bool:
    assert isinstance(path, str)

    return os.path.exists(path)


def joinpath(dirname: str, fname: str) -> str:
    assert isinstance(dirname, str)
    assert isinstance(fname, str)

    return os.path.join(dirname, fname)


def make_dir(dirname: str) -> bool:
    assert isinstance(dirname, str)

    return os.makedirs(dirname)


def new_filename_by_input(title: str) -> str:
    assert isinstance(title, str)

    return input(f"> Please Enter the new file name of {title}: ")
