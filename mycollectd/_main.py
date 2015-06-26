import argparse
import datetime
import json
import pkg_resources
import re
import sys
import os


from .battery import sample_battery
from .ping import sample_ping
from .smc import sample_smc
from .airport import sample_airport
from .airportscan import sample_airportscan

samplers = [sample_battery, sample_ping, sample_smc, sample_airport, sample_airportscan]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--exclude')
    parser.add_argument('-t', '--types')
    parser.add_argument('-i', '--indent', action='store_true')
    parser.add_argument('-d', '--out-dir')
    parser.add_argument('-f', '--format', default='%Y-%m-%d.log')
    args = parser.parse_args()

    # determine which types to sample (None -> all)
    types_to_sample = set(re.split(r'\W+', args.types)) if args.types else None
    types_to_exclude = set(re.split(r'\W+', args.exclude or ''))

    # get the output file handle
    if args.out_dir:
        path = os.path.join(args.out_dir, datetime.datetime.utcnow().strftime(args.format))
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        output = open(path, 'ab')
    else:
        output = sys.stdout

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
                res.setdefault('_time', datetime.datetime.utcnow().isoformat('T'))
                encoded_res = json.dumps(res, sort_keys=True, indent=4 if args.indent else None)
        except Exception as e:
            res = dict(type=name, error_type=e.__class__.__name__, error=str(e))
            encoded_res = json.dumps(res)

        if res:
            output.write(encoded_res + '\n')

    output.flush()




