from subprocess import Popen, PIPE
from plistlib import readPlistFromString as plist_loads
import pprint

KEYS = '''
    Amperage
    AvgTimeToEmpty
    AvgTimeToFull
    CellVoltage
    CurrentCapacity
    CycleCount
    DesignCapacity
    InstantAmperage
    InstantTimeToEmpty
    MaxCapacity
    Temperature
    TimeRemaining
    Voltage
'''.strip().split()


def sample_airport():

    proc = Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    if proc.returncode:
        return
    if not out:
        return

    res = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        key, value = line.split(': ', 1)
        try:
            value = int(value)
        except ValueError:
            pass

        res[key] = value

    return res
    


