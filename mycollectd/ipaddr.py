import urllib
import json


def sample_ipaddr():
    res = urllib.urlopen('https://httpbin.org/ip')
    data = json.loads(res.read())
    data['ipaddr'] = data.pop('origin')
    return data

