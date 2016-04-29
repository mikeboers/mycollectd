import argparse
import datetime
import json
import os
import pkg_resources
import re
import sys

from .utils import get_output_fh

from .battery import sample_battery
from .ping import sample_ping
from .smc import sample_smc
from .airport import sample_airport
from .airportscan import sample_airportscan
from .timezone import sample_timezone
from .ipaddr import sample_ipaddr

samplers = [
    sample_battery,
    sample_ping,
    sample_smc,
    sample_airport,
    sample_airportscan,
    sample_timezone,
    sample_ipaddr,
]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--exclude')
    parser.add_argument('-t', '--types')
    parser.add_argument('-i', '--indent', action='store_true')
    parser.add_argument('-d', '--out-dir')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()

    # determine which types to sample (None -> all)
    types_to_sample = set(re.split(r'\W+', args.types)) if args.types else None
    types_to_exclude = set(re.split(r'\W+', args.exclude or ''))

    output = get_output_fh(args.out_dir, args.format)

    for func in samplers:

        name = re.sub(r'^sample_', '', func.__name__)

        # only run the requested types
        if name in types_to_exclude:
            continue
        if types_to_sample is not None and name not in types_to_sample:
            continue

        try:
            res = func()
            if res:
                res.setdefault('_type', name)
                res.setdefault('_time', datetime.datetime.utcnow().isoformat('T') + 'Z')
                encoded_res = json.dumps(res, sort_keys=True, indent=4 if args.indent else None)
        except Exception as e:
            res = dict(type=name, error_type=e.__class__.__name__, error=str(e))
            encoded_res = json.dumps(res)

        if res:
            output.write(encoded_res + '\n')

    output.close()




