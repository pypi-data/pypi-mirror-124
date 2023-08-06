"""
Simplified data fitting.

Uses scipy.optimize.curve_fit (no x errors) or scipy.odr (with x errors).
"""
from .fit import auto, fit, data_split
__all__ = ['auto', 'fit', 'data_split']
