import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib
from matplotlib import colors as mcolors
from uncertainties.unumpy import nominal_values as unv
#from uncertainties.unumpy import std_devs as usd
from smpl2 import io, fit

def set_plot_style(**params):
    """
    fig_labelsize = 12
    ‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’, ‘x-large’, ‘xx-large’.
    """
    pylab.rcParams.update(params)
    matplotlib.rcParams.update(params)

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
default_params = {'legend.fontsize': 'x-large',
                  'figure.figsize': (8, 6),
                  'axes.labelsize': 'x-large',
                  'axes.titlesize':'x-large',
                  'xtick.labelsize':'x-large',
                  'ytick.labelsize':'x-large'}
set_plot_style(**default_params)

#@append_doc(default_kwargs)
def plt_data(datax, datay, plt_xerr=None, plt_yerr=None, color="C0", zorder=20, range=(None,None), selector=None, **kwargs):
    """
    Plot ``datay`` against ``datax`` with error bars.
    For more parameters look at ``matplotlib.pyplot.errorbar``.

    Parameters
    ----------
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    plt_xerr : bool, optional
        Whether uncertainties of ``datax`` should be plottet.
        If ``None``: plot if ``datax`` has ANY uncertainties.
        The default is None.
    plt_yerr : bool, optional
        Whether uncertainties of ``datay`` should be plottet.
        If ``None``: plot if ``datay`` has ANY uncertainties.
        The default is None.
    color : str, optional
        Color of the data-points. The default is "C0".
    zorder : float, optional
        Order in which plots should be drawn.
        Higher values will be drawn on top of others.
        The default is 20.
    range : (low, high), optional
        Lower and higher bounds of data used.
        Applied BEFORE selector.
        The default is (None,None).
    selector : [bool] or f(x, y) -> [bool], optional
        Either a mask for data used or a function(datax, datay) returning the mask.
        Applied AFTER range slicing.
        The default is None.
    **kwargs : dict
        Further arguments for plotting with ``matplotlib.pyplot.errorbar``.
    """
    assert len(datax) == len(datay)
    x, y, xerr, yerr = fit.data_split(datax, datay, range=range, selector=selector, mode='any')
    if plt_xerr is False: xerr = None
    if plt_yerr is False: yerr = None
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, zorder=zorder **kwargs)

def plt_error(datax, datay, sigma=1, alpha=0.4, alphaData=0.7, label=None, color="C1", zorder=10, filltype="y", range=(None,None), selector=None, **kwargs):
    """
    Plot ``datay`` against ``datax`` and colorize region of uncertainty.
    For more parameters look at ``matplotlib.pyplot.plot`` and ``matplotlib.pyplot.fill_between``.

    Parameters
    ----------
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    sigma : float, optional
        Region which will be colorized. The default is 1.
    alpha : float, optional
        alpha value of uncertainty. The default is 0.4.
    alphaData : float, optional
        alpha value of function values. The default is 0.7.
    label : str, optional
        string to be shown in legend. The default is None.
    color : str, optional
        color used for function and uncertainty. The default is "C1".
    zorder : float, optional
        Order in which plots should be drawn.
        Higher values will be drawn on top of others.
        The default is 10.
    filltype : 'x', 'y', optional
        Whether to use the uncertainties of ``datax`` or ``datay``.
        The default is "y".
    range : (low, high), optional
        Lower and higher bounds of data used.
        Applied BEFORE selector.
        The default is (None,None).
    selector : [bool] or f(x, y) -> [bool], optional
        Either a mask for data used or a function(datax, datay) returning the mask.
        Applied AFTER range slicing.
        The default is None.
    """
    if label is not None: label += r"$\pm %s\sigma$" % sigma
    x, y, xerr, yerr = fit.data_split(datax, datay, range=range, selector=selector, mode='no')
    plt.plot(x, y, alpha=alphaData, label=label, color=color, zorder=zorder+1, **kwargs)
    if filltype == "y":
        plt.fill_between(x, y - sigma*yerr, y + sigma*yerr, alpha=alpha, color=color, zorder=zorder, **kwargs)
    if filltype == "x":
        plt.fill_betweenx(y, x - sigma*xerr, x + sigma*xerr, alpha=alpha, color=color, zorder=zorder, **kwargs)

def plt_function(func, xmin, xmax, *args, num=50, **kwargs):
    """
    Plot function ``func`` between ``xmin`` and ``xmax``.

    Parameters
    ----------
    func : callable(x, *args)
        function for the Y-data.
    xmin : number
        lower bound for the X-data.
    xmax : number
        upper bound for the X-data.
    *args : tuple
        arguments for ``func``.
    num : int, optional
        data points used for X-data. The default is 50.
    **kwargs : TYPE
        further arguments for plotting with ``plt_error``.
    """
    x = np.linspace(xmin, xmax, num)
    y = func(x, *args)
    plt_error(x, y, **kwargs)

def plt_residuals(datax, datay, func, *args, **kwargs):
    """
    Plot the residuals between ``datay`` and ``func``.

    Parameters
    ----------
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    func : callable(x, *args)
        function to calculate residuals.
    *args : tuple
        arguments for ``func``.
    **kwargs : dict
        further arguments for plotting with ``plt_data``.
    """
    fity = func(datax, *args)
    res = datay - fity
    plt_data(datax, res, **kwargs)

def init(**kwargs):
    """
    Init a new plot and set standard parameters.

    Parameters
    ----------
    **kwargs :
        Parameters for ``matplotlib.pyplot.figure``.

    Returns
    -------
    fig :
        The newly created figure.
    """
    fig = plt.figure(**kwargs)
    params(grid=True, legend=True, tick_params='both', direction='in', tight_layout=True)
    return fig

def params(xlabel=None, ylabel=None, xlim=None, ylim=None, grid=None, legend=None, tick_params=None, tight_layout=None, xscale=None, yscale=None, title=None, minorticks=None, **kwargs):
    """
    Sets basic parameters for a plot.
    Multiple parameters can be edited simultaneously.
    If parameters are None, nothing will be changed.
    More control is provided through **kwargs.

    Parameters
    ----------
    xlabel : str, optional
        Sets the x-axis label.
    ylabel : str, optional
        Sets the y-axis label.
    xlim : (float,float), optional
        Sets the drawing range of the x-axis.
    ylim : (float,float), optional
        Sets the drawing range of the y-axis.
    grid : bool, optional
        If a grid should be drawn.
    legend : bool, optional
        If a legend should be drawn.
    tick_params : 'x', 'y', 'both', optional
        Sets the axis ticks.
    tight_layout : bool, optional
        If a tight layout should be used.
    xscale : "linear", "log", "symlog", "logit", optional
        Sets the scale layout for the x-axis.
    yscale : "linear", "log", "symlog", "logit", optional
        Sets the scale layout for the y-axis.
    title : str, optional
        Shows a title above the plot.
    **kwargs : TYPE
        Further parameters are passed to every function.
    """
    if xlabel is not None: plt.xlabel(xlabel, **kwargs)
    if ylabel is not None: plt.ylabel(ylabel, **kwargs)
    if xlim is not None: plt.xlim(xlim, **kwargs)
    if ylim is not None: plt.ylim(ylim, **kwargs)
    if grid is not None: plt.grid(grid, **kwargs)
    if legend is not None: plt.legend(**kwargs) # prop={'size':fig_legendsize},
    if tick_params is not None: plt.tick_params(tick_params, **kwargs)
    if tight_layout is not None: plt.tight_layout()
    if xscale is not None:
        if xscale == "log" and "nonposx" not in kwargs:
            kwargs["nonposx"] = "clip"
        plt.xscale(xscale, **kwargs)
    if yscale is not None:
        if yscale == "log" and "nonposy" not in kwargs:
            kwargs["nonposy"] = "clip"
        plt.yscale(yscale, **kwargs)
    if title is not None: plt.title(title, **kwargs)
    if minorticks is not None: plt.minorticks_on() if minorticks else plt.minorticks_off()

def save(file, *formats, **kwargs):
    """
    Save the currently active plot into a file.
    **kwargs are passed to plt.savefig

    Parameters
    ----------
    file : str
        path and name of file.
    *formats : str, optional
        Plot is saved in all given formats.
        The defaults are "png" and "pdf".
    """
    if len(formats) == 0: formats = "png", "pdf"
    io.mkdirs(file)
    for f in formats:
        plt.savefig("{file}.{ending}".format(file=file, ending=f), **kwargs)

def finish(show=True):
    """
    Finish the currently active plot and close it.

    Parameters
    ----------
    show : bool, optional
        If the plot should be shown in console. The default is True.
    """
    if show: plt.show()
    plt.close()

# ========================================================
# ========   convenience methods   =======================
# ========================================================

#@append_doc(default_kwargs)
def fit_plot(datax, datay, function, params=None, **kwargs):
    """Fit function to datax and datay.
    Then plot both data and resulting function.

    Parameters
    ==========
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    function : func
        Fit function with parameters: ``x``, ``*params``
        Fit parameters can be fixed via ``**kwargs`` eg. ``a=5`` and setting ``fixed_params=True``.
    params : tuple, optional
        starting fit parameters. None will let the fit method choose the parameters.

    Returns
    -------
    ffit : f(x) -> y
        optimized function.
    pfit : tuple
        optimized fit parameters.
    """
    ffit, pfit = fit.fit(datax, datay, function, params=params, **kwargs)
    plt_data(datax, datay, **kwargs)
    plt_function(ffit, unv(np.min(datax)), unv(np.max(datay)), **kwargs)
    return ffit, pfit

if __name__ == "__main__":
    import doctest
    doctest.testmod()
