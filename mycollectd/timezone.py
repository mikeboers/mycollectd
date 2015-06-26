import time


def sample_timezone():
    localtime = time.localtime()
    is_dst = localtime.tm_isdst > 0
    return {
        'name': time.tzname[int(is_dst)],
        'offset': -time.altzone if is_dst else -time.timezone,
    }
