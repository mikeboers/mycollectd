from subprocess import Popen, PIPE
from plistlib import readPlistFromString as plist_loads


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


def sample_battery():

    proc = Popen(['/usr/sbin/ioreg', '-arn', 'AppleSmartBattery'], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    if proc.returncode:
        return

    data = plist_loads(out)[0]
    
    return dict((k, data[k]) for k in KEYS)


