try:
    import psutil
except ImportError:
    psutil = None

def sample_netio():
    if psutil:
        io = psutil.net_io_counters()
        return dict(vars(io))
