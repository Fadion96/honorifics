import re

pattern_time = re.compile(r'\d+')


def from_ass_to_cs(time: str) -> int:
    new_time = tuple(map(int, pattern_time.findall(time)))
    return new_time[3] + new_time[2] * 100 + new_time[1] * 6000 + new_time[0] * 360000


def from_cs_to_ass(time: int) -> str:
    hours = int(time / 360000)
    time -= hours * 360000
    minutes = int(time / 6000)
    time -= minutes * 6000
    seconds = int(time / 100)
    time -= seconds * 100

    return str(hours) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2) + '.' + str(time).zfill(2)


frame_rate = 23.976

_conversion_table = {
    '.ass': {
        'cs': from_ass_to_cs
    },
    'frame': {
        'cs': lambda x: int(100 * x / frame_rate)
    },
    'cs': {
        '.ass': from_cs_to_ass,
        'cs': lambda x: x
    },
    'ms': {
        'cs': lambda x: int(x / 10)
    }
}


def change_time(time_a, unit_a: str, time_b, unit_b: str, unit_out: str):
    shared = set(
        _conversion_table[unit_a].keys() & _conversion_table[unit_b].keys() & _conversion_table[unit_out].keys()
    ).pop()

    return _conversion_table[shared][unit_out](
        _conversion_table[unit_a][shared](time_a) + _conversion_table[unit_b][shared](time_b)
    )
