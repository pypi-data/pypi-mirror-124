import numpy as np
from numpy.linalg import LinAlgError
from scipy import optimize
from scipy.odr import Model, RealData, ODR
import uncertainties as unc
from uncertainties.unumpy import nominal_values as unv
from uncertainties.unumpy import std_devs as usd
# local imports
from smpl.functions import polN, order, cos, lorentz, gauss, split_gauss
from smpl.util import reduce_function, unv_lambda, uncertain

default_funcs = [polN(3), order, cos, lorentz, gauss, split_gauss]

def auto(datax, datay, *funcs, **kwargs):
    """
    Automatically loop over ``funcs`` and fit the best one.
    If no functions are given, use ``default_funcs``.
    """
    min_sq = None
    if len(funcs) == 0:
        funcs = default_funcs
    for f in funcs:
        if not callable(f): continue
        try:
            ff, fp = fit(datax, datay, f, **kwargs)
            fy = ff(datax)
        except (ValueError, LinAlgError):
            continue
        if uncertain(fy): # weighted residuals + favour small uncertainties
            sum_sq = np.sum((fy - datay)**2 / (usd(datay)**2 + usd(fy)**2)) \
                   + np.sum(usd(fy)**2 / usd(datay)**2)
        else:
            sum_sq = np.sum((fy - datay)**2)
        if min_sq is None or sum_sq < min_sq:
            min_sq = sum_sq
            best = f, fp, ff
    return best

def fit(datax, datay, function, params=None, fixed_params=True, **kwargs):
    """
    Returns a fit of ``function`` to ``datax`` and ``datay``.
    Use ``_fit_odr`` or ``_fit_curvefit`` respectively if ``datay`` has or has not uncertainties.

    Parameters
    ==========
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``
    function : func
        Fit function with parameters: ``x``, ``*params``
    params : tuple, optional
        starting fit parameters. None will let the fit method choose the parameters.
    fixed_params : bool, optional
        Whether to use fixed parameters in ``function``. The default is True.
    **kwargs : TYPE
        fixed parameters for ``function``, as well as for ``data_split`` and fit-method.

    Returns
    -------
    ffit : f(x) -> y
        optimized function.
    pfit : tuple
        optimized fit parameters.
    """
    x, y, xerr, yerr = data_split(datax, datay, **kwargs)

    if fixed_params:
        function = reduce_function(function, **kwargs)

    if xerr is not None:
        pfit = _fit_odr(x, y, unv_lambda(function), params=params, xerr=xerr, yerr=yerr, **kwargs)
    else:
        pfit = _fit_curvefit(x, y, unv_lambda(function), params=params, yerr=yerr, **kwargs)

    return lambda x: function(x, *pfit), pfit

def data_split(datax, datay, range=(None,None), selector=None, mode='all', **kwargs):
    """
    Splits datax and datay into (x, y, xerr, yerr).
    Select data with range and selector.

    Parameters
    ----------
    datax : array_like
        X data either as ``unp.uarray`` or ``np.array`` or ``list``.
    datay : array_like
        Y data either as ``unp.uarray`` or ``np.array`` or ``list``.
    range : (low, high), optional
        lower and higher bounds of data used.
        Applied BEFORE selector.
        The default is (None,None).
    selector : [bool] or f(x, y) -> [bool], optional
        Either a mask for data used or a function(datax, datay) returning the mask.
        Applied AFTER range slicing.
        The default is None.
    mode : 'all', 'any', 'none', _, optional
        How the uncertainties should be handled:
         - ``all``: only keep uncertainties if all data has them
         - ``any``: if any data has uncertainties, keep them
         - ``none``: always remove the uncertainties
         - _ : anything else will always keep the uncertainties
        The default is ``all``.

    Returns
    -------
    x : TYPE
        nominal values of xdata.
    y : TYPE
        nominal values of ydata.
    xerr : TYPE
        uncertainty of datax.
    yerr : TYPE
        uncertainty of datay.
    """
    assert len(datax) == len(datay)
    low, high = range
    if low is None: low = 0
    if high is None: high = len(datax)
    s = slice(low,high)
    datax, datay = datax[s], datay[s]

    x, y, xerr, yerr = unv(datax), unv(datay), usd(datax), usd(datay)
    if selector is not None:
        mask = selector(datax, datay) if callable(selector) else selector
        assert len(mask) == len(datax)
        x, y, xerr, yerr = x[mask], y[mask], xerr[mask], yerr[mask]
    a = any if mode=='any' else all if mode=='all' else lambda x: mode=='none'
    if a(xerr == 0): xerr = None # if ANY or ALL value is invalid, remove uncertainty
    if a(yerr == 0): yerr = None
    return x, y, xerr, yerr

# https://stackoverflow.com/questionsquestions/14581358/getting-standard-errors-on-fitted-parameters-using-the-optimize-leastsq-method-i#
# Updated on 4/6/2016
# User: https://stackoverflow.com/users/1476240/pedro-m-duarte
def _fit_curvefit(datax, datay, function, params=None, yerr=None, epsfcn=0.0001, maxfev=10000, **kwargs):
    try:
        pfit, pcov = optimize.curve_fit(function, datax, datay, p0=params, sigma=yerr, epsfcn=epsfcn, maxfev=maxfev, **kwargs)
    except RuntimeError:
        return params
    return unc.correlated_values(pfit,pcov)

# Note Issues on scipy odr and curve_fit, regarding different definitions/namings of standard deviation or error and covaraince matrix
# https://github.com/scipy/scipy/issues/6842
# https://github.com/scipy/scipy/pull/12207
# https://stackoverflow.com/questions/62460399/comparison-of-curve-fit-and-scipy-odr-absolute-sigma
def _fit_odr(datax, datay, function, params=None, yerr=None, xerr=None):
    model = Model(lambda p,x : function(x,*p))
    realdata = RealData(datax, datay, sy=yerr, sx=xerr)
    odr = ODR(realdata, model, beta0=params)
    out = odr.run()
    return unc.correlated_values(out.beta, out.cov_beta)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
