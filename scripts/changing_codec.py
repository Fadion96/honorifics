#!/usr/bin/env python3
import os
import argparse
import sys

sys.path.insert(0, '../honorifics')
from honorifics.codec_changer import CodecChanger


def parse_arg():
    parser = argparse.ArgumentParser(description="Codec changer with negate filter at the given timestamps")
    parser.add_argument("input_video", type=str, help="Input video")
    parser.add_argument("-timestamp", "-t", type=str, action='append', metavar=('start', 'end'), help="Timestamp in seconds", nargs=2)
    parser.add_argument("-output", "-o", metavar='output', nargs="?", type=str, help="Output video",
                        default="output.mkv")
    parser.add_argument("-subtitles", "-s", metavar="subtitles", type=str, help="subtitles to be hardsubbed")
    parser.add_argument("-deband", "-de", action='store_true')
    parser.add_argument("-f", "-from", type=str, nargs=1, metavar='start', help="Video start time")
    parser.add_argument("-to", type=str, nargs=1, metavar='end', help="Video end time")
    return parser.parse_args()


def hms_to_seconds(timestamp):
    t = 0
    for u in timestamp.split(':'):
        t = 60 * t + float(u)
    return t


if __name__ == '__main__':
    args = parse_arg()
    timestamps = []
    if args.timestamp:
        for s in args.timestamp:
            times = []
            for x in s:
                seconds = hms_to_seconds(x)
                times.append(seconds)
            timestamps.append(times)
    print(timestamps)
    if args.f:
        start = hms_to_seconds(args.f[0])
    else:
        start = 0
    if args.to:
        end = hms_to_seconds(args.to[0])
    else:
        end = 0
    subs = args.subtitles.replace('\\', '\\\\\\\\').replace(':', '\\\\:')
    changer = CodecChanger(args.input_video, args.output,
                           args.deband, subtitles=subs,
                           timestamps=timestamps, start=start, end=end)
    command = changer.make_command()
    print("\n", command, "\n")
    os.system(command)
