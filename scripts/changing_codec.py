#!/usr/bin/env python3
import os
import argparse


def parse_arg():
    parser = argparse.ArgumentParser(description="Codec changer with negate filter at the given timestamps")
    parser.add_argument("input_video", type=str, help="Input video")
    parser.add_argument("timestamp", type=int, help="Timestamp in seconds", nargs='*')
    parser.add_argument("-duration", "-d", nargs='*', type=int, help="Duration of negation in seconds (default = 10)", default=[10])
    parser.add_argument("-output", "-o", metavar='output', nargs="?", type=str, help="Output video",
                        default="output.mkv")
    parser.add_argument("-subtitles", "-s", metavar="subtitles", type=str, help="subtitles to be hardsubbed")
    return parser.parse_args()


def start_of_video(first_timestamp):
    return "\"[0:0]trim=start=0:duration=" + str(first_timestamp) + "[a];", "[a]"


def negation_part(timestamp, duration, last_part, number):
    result = "[0:0]trim=start=" + str(timestamp) + ":duration=" + str(duration) + ",setpts=PTS-STARTPTS[trimmed" + str(
        number) + "];"
    result += "[trimmed" + str(number) + "]negate[negation" + str(number) + "];"
    result += last_part + "[negation" + str(number) + "]concat[negated" + str(number) + "];"
    return result, "[negated" + str(number) + "]"


def normal_part(timestamp, duration, last_part, number):
    result = "[0:0]trim=start=" + str(timestamp) + ":duration=" + str(duration) + ",setpts=PTS-STARTPTS[nor" + str(
        number) + "];"
    result += last_part + "[nor" + str(number) + "]concat[normal" + str(number) + "];"
    return result, "[normal" + str(number) + "]"


def end_of_video(timestamp, last_part):
    result = "[0:0]trim=start=" + str(timestamp) + ",setpts=PTS-STARTPTS[ending];"
    result += last_part + "[ending]concat[out1]\" "
    return result


def end_of_video_subs(timestamp, last_part, subtitles):
    result = "[0:0]trim=start=" + str(timestamp) + ",setpts=PTS-STARTPTS[ending];"
    result += last_part + "[ending]concat[subs];"
    result += "[subs]ass=" + subtitles.replace(".\\", "") + "[out1]\" "
    return result


def main(arguments):
    first_pass = "ffmpeg -y -i " + arguments.input_video
    second_pass = " && ffmpeg -y -i " + arguments.input_video
    if arguments.timestamp:
        if len(arguments.timestamp) > len(arguments.duration):
            diff = len(arguments.timestamp) - len(arguments.duration)
            arguments.duration.extend([10]*diff)
        filter_complex = " -filter_complex "
        start, last_part = start_of_video(arguments.timestamp[0])
        filter_complex += start
        for i in range(len(arguments.timestamp)-1):
            negation, last_part = negation_part(arguments.timestamp[i], arguments.duration[i], last_part, i)
            filter_complex += negation
            normal_timestamp = arguments.timestamp[i] + arguments.duration[i]
            normal, last_part = normal_part(normal_timestamp, arguments.timestamp[i+1] - normal_timestamp, last_part, i)
            filter_complex += normal
        last_index = len(arguments.timestamp) - 1
        last_negation, last_part = negation_part(arguments.timestamp[last_index], arguments.duration[last_index], last_part, last_index)
        filter_complex += last_negation
        if arguments.subtitles:
            end = end_of_video_subs(arguments.timestamp[last_index] + arguments.duration[last_index], last_part, arguments.subtitles)
        else:
            end = end_of_video(arguments.timestamp[last_index] + arguments.duration[last_index], last_part)
        filter_complex += end
        filter_complex += "-map [out1]"
        first_pass += filter_complex
        second_pass += filter_complex
    else:
        if arguments.subtitles:
            first_pass += " -vf \"ass=" + arguments.subtitles.replace(".\\", "") + "\" "
            second_pass += " -vf \"ass=" + arguments.subtitles.replace(".\\", "") + "\" "
    first_pass += " -c:v libvpx-vp9 -pass 1 -pix_fmt yuv420p -crf 21 -threads 3 -speed 4 -tile-columns 6 -frame-parallel 1 -b:v 0 -an -f matroska /dev/null"
    second_pass += " -c:v libvpx-vp9 -pass 2 -pix_fmt yuv420p -crf 21 -threads 3 -speed 1 -tile-columns 6 -frame-parallel 1 -b:v 0 -auto-alt-ref 1 -lag-in-frames 25 -an -f matroska " + arguments.output
    command = first_pass + second_pass
    os.system(command)


if __name__ == '__main__':
    args = parse_arg()
    main(args)
