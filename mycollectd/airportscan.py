from subprocess import Popen, PIPE
from plistlib import readPlistFromString as plist_loads


def sample_airportscan():

    proc = Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-xs'], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    if proc.returncode:
        return
    if not out:
        return
    
    networks = []
    
    for data in plist_loads(out):
        networks.append({
            'ssid': data['SSID_STR'],
            'bssid': data['BSSID'],
            'rssi': data['RSSI'],
        })

    return {'networks': networks}


