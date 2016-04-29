import os

def sample_loadavg():
    _1, _5, _15 = os.getloadavg()
    return {
        'loadavg_1m': _1,
        'loadavg_5m': _5,
        'loadavg_15m': _15,
    }

