def _edit(txt,append=True):
    """
    Inserts the given docstring text ``txt`` at the beginning or end of the ``target`` docstring.
    """
    def wrapper(target):
        docstr = txt(target) if callable(txt) else txt
        if target.__doc__ is None:
            target.__doc__ = ""
        if append: target.__doc__ += '\n' + docstr
        else: target.__doc__ = docstr + '\n' + target.__doc__
        return target
    return wrapper

def append_str(txt):
    """
    Append a string at the end of the ``target`` docstring.
    """
    return _edit(txt)

def append_plot(*args,xmin=-5,xmax=5):
    """
    Append a plot at the end of the ``target`` docstring.
    """
    docstr = lambda target: "\n\n\t.. plot::\n\t\t:include-source:\n\n\t\t>>> from " + target.__module__ + " import " +target.__name__ + "\n\t\t>>> from smpl import plot\n\t\t>>> plot.function("+ target.__name__ + "," + ','.join([str(a) for a in args]) + ",xmin="+str(xmin) + ",xmax=" + str(xmax)+")"
    return _edit(docstr)

def append_doc(original):
    """
    Append docstring of ``original`` to the end of ``target`` docstring.
    """
    return _edit(original.__doc__)

def insert_str(txt):
    return _edit(txt, append=False)

def insert_doc(original):
    """
    Inserts the docstring from passed function ``original`` in front of the ``target`` function docstring.
    """
    return _edit(original.__doc__, append=False)

def insert_latex(latex,definition=True):
    """
    Inserts the function definition and a latex representation in front of the ``target`` docstring.
    """
    def docstr(target):
        if definition: return target.__name__ + "(" + ", ".join(target.__code__.co_varnames) + ") = \n..math::\n\t" + latex
        else: return "..math::\n\t" + latex
    return _edit(docstr, append=False)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    