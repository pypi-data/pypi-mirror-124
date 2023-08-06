import pathlib
import os
import sys
from smpl2 import debug

def pwd():
    """
    Returns the path to the path of current file
    """
    return "/".join(debug.get_line_number_file(split=False,_back=1)[1].split("/")[:-1])

def import_path(path='../..'):
    """
    Adds ``path`` to the ``sys.path``
    """
    sys.path.insert(0, os.path.abspath(path))

def mkdirs(fn):
    '''
    Creates the neccessary directories above ``fn``.
    '''
    pathlib.Path(fn).parent.mkdir(parents=True, exist_ok=True)

def pr(*args, end='\n'):
    """
    Prints and returns the passed ``args``.
    """
    print(*args,end=end)
    return args

def files(folder, ending=''):
    """
    Get all the files in ``folder`` ending with ``ending``.
    """
    r = []
    for file in os.scandir(folder):
        if file.path.endswith(ending):
            r.append(os.path.splitext(os.path.basename(file.path))[0],file.path)
    return r

def out(filename, txt):
    """
    Saves ``str(txt)`` into given filename and returns the object.
    """
    mkdirs(filename)
    with open(filename,"w") as file:
        s = str(txt)
        file.write(s)
    return txt

def dump(directory, **kwargs):
    """
    Writes all variables in ``kwargs`` into ``directory``.
    Dump ``globals``, if no variables are given.
    """
    if len(kwargs) == 0:
        kwargs = globals()
    for key, val in kwargs.items():
        out(directory + '/' + key, val)
