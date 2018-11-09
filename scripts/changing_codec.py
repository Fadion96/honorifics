#!/usr/bin/env python3
import os
import argparse
import sys

sys.path.insert(0, '../honorifics')
from honorifics.codec_changer import CodecChanger


def parse_arg():
    parser = argparse.ArgumentParser(description="Codec changer with negate filter at the given timestamps")
    parser.add_argument("input_video", type=str, help="Input video")
    parser.add_argument("timestamp", type=str, help="Timestamp in seconds", nargs='*')
    parser.add_argument("-duration", "-d", nargs='*', type=str, help="Duration of negation in seconds (default = 10)",
                        default=[])
    parser.add_argument("-output", "-o", metavar='output', nargs="?", type=str, help="Output video",
                        default="output.mkv")
    parser.add_argument("-subtitles", "-s", metavar="subtitles", type=str, help="subtitles to be hardsubbed")
    parser.add_argument("-deband", "-de", action='store_true')
    return parser.parse_args()


def hms_to_seconds(timestamp):
    t = 0
    for u in timestamp.split(':'):
        t = 60 * t + float(u)
    return t


if __name__ == '__main__':
    args = parse_arg()
    times = []
    durations = []
    if len(args.timestamp) > len(args.duration):
        diff = len(args.timestamp) - len(args.duration)
        args.duration.extend(["10"] * diff)
    for s in args.timestamp:
        seconds = hms_to_seconds(s)
        times.append(seconds)
    for d in args.duration:
        duration_seconds = hms_to_seconds(d)
        durations.append(duration_seconds)
    changer = CodecChanger(args.input_video, args.output,
                           args.deband, subtitles=args.subtitles,
                           timestamps=times, durations=durations)
    command = changer.make_command()
    print("\n", command, "\n")
    os.system(command)
