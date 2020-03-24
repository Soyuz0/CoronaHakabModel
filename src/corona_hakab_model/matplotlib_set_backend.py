# setting backend for matplotlib
try:
    import PySide2  # noqa: F401
except ImportError:
    pass
else:
    try:
        import matplotlib
    except ImportError:
        pass
    else:
        matplotlib.use("Qt5Agg")
