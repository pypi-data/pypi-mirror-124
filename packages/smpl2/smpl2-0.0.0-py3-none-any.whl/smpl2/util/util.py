import numpy as np
from smpl.latex import latexify
from uncertainties.unumpy import nominal_values as unv
from uncertainties.unumpy import std_devs as usd

def get(key,dic,default):
    """
    Returns dic[key] if this exists else default.
    """
    return dic[key] if has(key,dic) else default

def has(key, dic):
    """
    Checks if the key is in the dict and not None.
    """
    return key in dic and not dic[key] is None

def true(key, dic):
    """
    Checks if the key is in the dict and not None and True.
    """
    return has(key,dic) and dic[key]

def table_str(table, start=True, end=True, indent='\t'):
    if isinstance(table, dict):
        table = [(key,*val) if hasattr(val, '__iter__') else (key,val) for key, val in table.items()]
    return ('='*64 + '\n' + indent if start else indent) + \
           ('\n' + indent).join(['\t'.join(line) for line in table]) + \
           ('\n' + '='*64 if end else '')

def find_nearest(array, value):
    """
    Returns the index and value of the item in ``array`` closest to ``value``.
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array(idx)

def uncertain(array, mode='all'):
    """True, if ALL pr ANY datapoints have uncertainties."""
    if mode == 'all': return not any(usd(array) == 0)
    return not all(usd(array) == 0)

def reduce_function(f, **kwargs):
    """
    Returns the same function, but without the fixed arguments in ``kwargs``.
    """
    args = [(a, kwargs[a] if a in kwargs else a) for a in f.__code__.co_varnames]
    newvar = [a for a,v in args if v is a]
    oldvar = ["%s=%s" % (a,v) for a,v in args]
    return eval("lambda {newvars}: f({oldvars})".format(newvars=','.join(newvar), oldvars=','.join(oldvar)))

def unv_lambda(f):
    """
    Returns a function which applies :func:`unv` on the result of ``f``
    """
    var = ','.join(f.__code__.co_varnames)
    return eval("lambda {var}: unv(f(var))".format(var=var))

def usd_lambda(f):
    """
    Returns a function which applies :func:`usd` on the result of ``f``
    """
    var = ','.join(f.__code__.co_varnames)
    return eval("lambda {var}: usd(f({var}))".format(var=var))

def get_func_description(function, pfit=None, units=None):
    """
    Returns a LaTeX string of the function and its parameters/units if provided.
    """
    name = function.__name__
    if name == "<lambda>": name = "\\lambda"
    equation = function.__doc__.split('\n')[0]
    pnames = function.__code__.co_varnames[1:]
    eq = "$%s(%s) = %s$" % (name,','.join(pnames),equation.replace('$',''))
    if pfit is None: return eq
    if units == None: units = ['']*len(pfit)
    assert len(pnames) == len(pfit) == len(units)
    var = ["$%s = %s %s$" % (n,latexify(v),u) for n,v,u in zip(pnames, pfit, units)]
    return eq + '\n' + '\n'.join(var)
    