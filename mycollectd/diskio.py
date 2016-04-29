try:
    import psutil
except ImportError:
    psutil = None

def sample_diskio():
    if psutil:
        io = psutil.disk_io_counters()
        return dict(vars(io))
