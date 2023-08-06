import os.path
import shutil


def check_file_exist(file):
    if os.path.isfile(file):
        return True
    else:
        return False


def check_dir_exist(dir):
    if os.path.isdir(dir):
        return True
    else:
        return False


def check_disk_usage(unit: str = "byte"):
    """res = (total, used, free)"""
    res = shutil.disk_usage("/")
    if unit.lower() == "kilobyte":
        return [(each / 1024) for each in res]
    elif unit.lower() == "megabyte":
        return [(each / 1024 / 1024) for each in res]
    elif unit.lower() == "gigabyte":
        return [(each / 1024 / 1024 / 1024) for each in res]
    else:
        return res
