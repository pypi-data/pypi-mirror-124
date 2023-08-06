import numpy as np
import uncertainties.unumpy as unp

from smpl import doc

@doc.append_plot(4)
def const(x, m):
    """$c$"""
    return np.ones(np.shape(x))*m

@doc.append_plot(2)
def linear(x, a):
    """$a \\cdot x$"""
    return a*x

@doc.append_plot(2,-1)
def line(x, a, b):
    """$a \\cdot x + b$"""
    return a*x + b

@doc.append_plot(3,0.02,3)
def cos_abs(x, a, f, phi):
    """$a \\cdot |\\cos(2πf(x-\\phi))|$"""
    return a * np.abs(unp.cos(2*np.pi*f*(x-phi)))

@doc.append_plot(3,0.02,3)
def cos(x, a, f, phi):
    """$a \\cdot \\cos(2πf(x-\\phi))$"""
    return a * unp.cos(2*np.pi*f*(x-phi))
@doc.append_plot(3,0.02,3)
def sin(x, a, f, phi):
    """$a \\cdot \\sin(2πf(x-\\phi))$"""
    return a * unp.sin(2*np.pi*f*(x-phi))
@doc.append_plot(3,0.02,3)
def tan(x, a, f, phi):
    """$a \\cdot \\tan(2πf(x-\\phi))$"""
    return a * unp.tan(2*np.pi*f*(x-phi))

@doc.append_plot(0,5,3,0)
def lorentz(x,x_0,A,d,y):
    """$\\frac{A}{\\pi d \\left(1 + \\left(\\frac{x-x_0}{d}\\right)^2 \\right)} + y$"""
    return 1/(np.pi*d*(1+(x-x_0)**2/d**2))*A + y

@doc.append_plot(0,5,3,0)
def gauss(x, x_0, A, d, y):
    """$A\\cdot \\exp\\left(\\frac{-(x-x_0)^2}{2d^2}\\right)+y$"""
    return A * unp.exp(-(x - x_0)**2 / 2 / d**2) + y

@doc.append_plot(0.5,4)
def exp(x, c, y_0):
    """$y_0 \\cdot \\exp(cx)$"""
    return unp.exp(c * x) * y_0

@doc.append_plot(0.5,4,xmin=0.1)
def log(x, c, y_0):
    """$y_0 \\cdot \\log(cx)$"""
    return unp.log(c * x) * y_0

@doc.append_plot(1,3.3,-1,xmin=0)
def order(x,x0,a,k,y):
    """$a \\cdot (x-x_0)^k + y_0$"""
    return a*(x-x0)**k+y

@doc.append_plot(1,3.3,0,xmin=0)
def sqrt(x,x0,a,b,y0):
    """$a \\sqrt{b \\cdot (x-x_0)} + y_0$"""
    return a*unp.sqrt(b*(x-x0)) + y0

@doc.append_plot(0,1,2,3,0)
def split_gauss(x,x0,a,d0,d1,y0):
    """$a \\cdot \\exp\\left(\\frac{-(x-x_0)^2}{2d_0^2}\\right)+y_0$, for $x>x_0$\n$a \\cdot \\exp\\left(\\frac{-(x-x_0)^2}{2d_1^2}\\right)+y_0$, for $x<x_0$"""
    return np.where(x>x0,gauss(x,x0,a,d0,y0), gauss(x,x0,a,d1,y0))

def pol1(N):
    """Returns a single polynomial of N-th order."""
    assert N > 0
    def pol(x,a,x0,y0):
        return a * (x-x0)**N + y0
    pol.__doc__ = "$a \\cdot (x-x_0)^{%i} + y_0$" % N
    return pol
def polN(N):
    """Returns a full polynomial up to N-th order."""
    assert N > 1
    func = '+'.join(["a{order}*x**{order}".format(order=i) for i in range(N,1,-1)]) + "+a1*x+a0"
    func = "lambda x,{var}: {func}".format(var=','.join(['a%i'%i for i in range(N+1)]), func=func)
    func = eval(func)
    func.__doc__ = '$' + ' + '.join(["a_{%i} \\cdot x^{%i}" % (i,i) for i in range(N,1,-1)]) + " + a_1 \\cdot x + a_0$"
    return func
