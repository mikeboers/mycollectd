import datetime
import errno
import os
import sys


def iter_raw_output(input_):

    date = None
    buffer_ = []

    for line in input_:

        try:
            new_date = datetime.datetime.strptime(line.strip(), '%Y-%m-%dT%H:%M:%S')
        except:
            pass
        else:
            if date:
                yield date, ''.join(buffer_)
            date = new_date
            buffer_ = []
            continue

        buffer_.append(line)


def get_output_fh(out_dir, format=None, time=None):

    if not out_dir:
        return sys.stdout

    format = format or '%Y/%m/%Y-%m-%d.log'
    time = time or datetime.datetime.utcnow()
    path = os.path.join(out_dir, time.strftime(format))

    try:
        os.makedirs(os.path.dirname(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return open(path, 'ab')