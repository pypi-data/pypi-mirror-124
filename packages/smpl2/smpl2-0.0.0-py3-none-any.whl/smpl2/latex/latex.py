from collections.abc import Iterable
from itertools import chain, count
from smpl.io import out
import numpy as np

def _filename(path, file):
    return path + ("" if path[-1] == "/" else "/") + file + ".txt"

def SI(*val, path=None, file=None, unit=None, bonus=None):
    """Print a value in SI notation to a file.

    Parameters
    ----------
    path : string
        The path of the output file.
        May be a full or a relative path.
    file : string
        The name of the output file.
    val : object, optional
        The value to be printed.
        May be empty for no value.
        The default is None.
    unit : string, optional
        The unit to be printed after the value.
        May be empty for no unit.
        The default is None.
    bonus : string, optional
        Some bonus parameters for the command.
        May be empty for no extra commands.
        The default is None.
    show : bool, optional
        If True, shows the printed output in the console.
        The default is False.
    """
    return out(_filename(path, file), toSI(val=val, unit=unit, bonus = bonus))

def toSI(val=None, unit=None, bonus=None):
    """Return the value in SI notation.

    Parameters
    ----------
    val : object, optional
        The value to be printed.
        May be empty for no value.
        The default is None.
    unit : string, optional
        The unit to be printed after the value.
        May be empty for no unit.
        The default is None.
    bonus : string, optional
        Some bonus parameters for the command.
        May be empty for no extra commands.
        The default is None.
    """
    bonus = "" if bonus is None else ("[%s]" % bonus)
    if val is not None and unit is not None:
        return "\\SI%s{%s}{%s}" % (bonus,latexify(val), unit)
    if val is not None and unit is None:
        return "\\num%s{%s}" % (bonus,latexify(val))
    if val is None and unit is not None:
        return "\\si%s{%s}" % (bonus, unit)
    return ""

def latexify(val, comma=False, parenthesis=True):
    """Return the refactored string of a value with uncertainty."""
    s = str(val)
    s = s.replace('+/-', ' \\pm ') # plus minus with latex notation
    if comma: s = s.replace('.', ',') # german comma, can be ignored in latex setup
    if parenthesis: s = s.replace('(', '') # remove parenthesis
    if parenthesis: s = s.replace(')', '') # remove parenthesis
    s = s.replace('*', ' \\cdot ') # latex dot as multiplication
    return s

def _depth(seq):
    """Calculates the depth of non string lists.
    https://stackoverflow.com/questions/6039103/counting-depth-or-the-deepest-level-a-nested-list-goes-to
    """
    if seq is None or isinstance(seq, str) or not isinstance(seq, Iterable):
        return 0
    seq = iter(seq)
    try:
        for level in count():
            seq = chain([next(seq)], seq)
            seq = chain.from_iterable(s for s in seq if isinstance(s, Iterable) and not isinstance(s, str))
    except StopIteration:
        return level
    else:
        return 0

def table(path, file, data, header=None, leader=None, unit=None, bonus=None, horizontal=False):
    """Prints all data from a 2d-array into a file.

    Parameters
    ----------
    data : 2d-listlike
        contains the data. May be anything printable.
    path : string
        the path of the output file.
    file : string
        the name of the output file.
    header : list, optional
        The content will be printed as a table header.
        The default is None.
    leader : list, optional
        The content will be printed in front of every row.
        The default is None.
    unit : list, optional
        The units of each column/row will be printed behind the values.
            - If None, no units are printed.
            - If a string, it will be used in every entry.
            - If a list, its elements will be used for every column/row respectively.
            - If a 2d-list, its elements will be used for every entry respectively.
        The default is None.
    bonus : list, optional
        The bonuses to be used as arguments in the SI-command.
        Same syntax as units.
        The default is None.
    horizontal : bool, optional
        If True, the units and bonuses will be printed transposed.
        The default is False.
    """
    trans = lambda a, b: a.T if b else a
    data = np.array(data)
    a,b = data.shape
    unit_depth = _depth(unit)
    unit = np.array([[unit]*b]*a) if unit_depth == 0 else trans(np.array([unit]*(b if horizontal else a)), horizontal) if unit_depth == 1 else np.array(unit)
    bonus_depth = _depth(bonus)
    bonus = np.array([[bonus]*b]*a) if bonus_depth == 0 else trans(np.array([bonus]*(b if horizontal else a)), horizontal) if bonus_depth == 1 else np.array(bonus)

    assert unit.shape == bonus.shape == data.shape
    if leader is not None:
        assert len(leader) == a
    data = [[toSI(val=data[i,j], unit=unit[i,j], bonus=bonus[i,j]) for j in range(b)] for i in range(a)]

    tab = "\\begin{tabular}{" + ("c|" if leader else "") + "c"*b + "}\n\\toprule\n"
    if header is not None:
        assert len(header) == (b if leader is None else b+1)
        tab += " & ".join(header) + "\\\\ \\midrule\n"
    for i in range(a):
        if leader:
            tab += leader[i] + " & "
        tab += " & ".join(data[i]) + "\\\\\n"
    tab += "\\bottomrule\n\\end{tabular}"
    return out(_filename(path, file), tab)
