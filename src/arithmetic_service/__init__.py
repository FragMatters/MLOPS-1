"""Arithmetic Service package."""

# Compatibility shim for pandas 3+ and evidently 0.4+
try:
    import pandas.core.dtypes.common as _c
    if not hasattr(_c, "infer_dtype_from_object"):
        _c.infer_dtype_from_object = lambda x: getattr(x, "dtype", type(x))
except ImportError:
    pass

__version__ = "0.1.0"
