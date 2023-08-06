import numpy as np
from  uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy
import math

unv=unp.nominal_values
usd=unp.std_devs

def poisson(n):
    """
    Return ``n`` with added poissonian uncertainties.
    """
    return unp.uarray(n, np.sqrt(n + (n==0 + 0)))

def normalize(data):
    """
    Remap the data to be in range of [0, 1].
    """
    return (data-unv(np.amin(data))) / unv(np.amax(data)-np.amin(data))

def _wmean(n, w=None):
    """
    Calculates the weighted mean value of ``n``.
    """
    if w==None: w = usd(n)
    return sum(w*n) / sum(w)

def weighted_mean(n, w=None, sample=True):
    """
    Return weighted mean of ``n`` with combined error of variance and unvertainties of ``n``.
    """
    assert len(n) > 1
    if w==None: w = 1/usd(n)**2 # weights of collection
    k = _wmean(n,w)  # weighted mean
    err = _wmean((unv(n) - unv(k))**2, w) # weighted mean square diff
    if sample: err *= 1 / (1 - _wmean(w,w)/sum(w)) # correction for sampling
    return ufloat(unv(k), math.sqrt(usd(k)**2 + err))

def noisy(x, mean=0, std=1):
    """
    Add normal noise to ``x``.
    """
    return x + np.random.normal(mean,std,len(x))

def fft(data):
    """
    Get fast-fourier spectrum in positive absolute range.
    """
    N = len(data)
    fft = scipy.fftpack.fft(data)
    return 2 * abs(fft[:N//2]) / N
