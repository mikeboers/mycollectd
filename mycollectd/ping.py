import re
from subprocess import Popen, PIPE

def parse_output(out):
    m = re.search(r'icmp_seq=(\d+) ttl=(\d+) time=([\d\.]+)', out)
    if m:
        seq, ttl, time = m.groups()
        return {
            'ttl': int(ttl),
            'time': float(time),
        }
    else:
        return {
            'ttl': -1,
            'time': -1,
        }

def sample_ping():

    proc = Popen(['/sbin/ping', '-m255', '-t5', '-nc1', '8.8.8.8'], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return parse_output(out)

