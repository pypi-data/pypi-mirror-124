import os
from sys import platform
from .argsguard import args_guard

if os.name == "posix":
    OS = "MACOSX" if platform == "darwin" else "LINUX"
    LINUX = False if platform == "darwin" else True
    MACOSX = True if platform == "darwin" else False
    WINDOWS = False
else:
    OS = "WINDOWS"
    LINUX = False
    MACOSX = False
    WINDOWS = True

def cls() -> None:
    """
    A way to clear the console screen
    """
    os.system("clear") if os.name == "posix" else os.system("cls")

clear = cls

def extract_file_type(file_location:str) -> str:
    """
    A function to return the type of file
    -> file_location: str = location of a file in string... ex : "C:\\abc\\abc\\file.xyz"
    ----
    => str: string of the file type, ex : "xyz"
    """

    if not isinstance(file_location,str):
        raise TypeError("file_location must be a string")

    try:
        return file_location.rsplit(".", 1)[1]
    except IndexError:
        raise ValueError(f"Invalid File Location : '{file_location}'")

def go_up_dir(dir_location:str) -> str:
    """
    A function to return the parent directory
    -> dir_location: str = location of a directory in string... ex : "C:\\abc\\cdef"
    ----
    => str: string of the parent directory, ex : "C:\\abc"
    """

    if not isinstance(dir_location, str):
        raise TypeError("dir_location must be a string")

    try:
        return dir_location.rsplit("/", 1)[0] if os.name == "posix" else dir_location.rsplit("\\", 1)[0]
    except Exception:
        raise ValueError(f"Invalid Directory Location : '{dir_location}'")

def dir2list(dir_location:str) -> list:
    """
    A function to return a given directory in the form of a list
    -> dir_location: str = location of a directory in string... ex : "C:\\abc\\cdef"
    ----
    => list: ex : ["C:", "abc", "cdef"]
    """

    if not isinstance(dir_location, str):
        raise TypeError("dir_location must be a string")

    try:
        return dir_location.split("/") if os.name == "posix" else dir_location.split("\\")
    except Exception:
        raise ValueError(f"Invalid Directory Location : '{dir_location}'")

def list2dir(dir_list:list) -> str:
    """
    A function to return a given list in the form of a directory
    -> dir_list: list = location of a directory in string... ex : ["C:", "abc", "bcd"]
    ----
    => str: ex : "C:\\abc\\bcd"
    """

    if not isinstance(dir_list, list):
        raise TypeError("dir_list must be a list")

    try:
        return "/".join(dir_list) if os.name == "posix" else "\\".join(dir_list)
    except Exception:
        raise ValueError(f"Invalid Directory Location : '{dir_list}'")
