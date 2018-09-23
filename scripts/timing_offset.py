#!/usr/bin/env python3
import sys, argparse
sys.path.insert(0, '../honorifics')

import honorifics.time_utils
from honorifics.subtitle_file_helper import SubStationFileHelper
from honorifics.substation_utils import EventDialogueTiming


parser = argparse.ArgumentParser()
parser.add_argument('-fps', type=float,
                    help='frame rate for calculating timing offset, default to: %.3f' % honorifics.time_utils.frame_rate)

args = parser.parse_args()

if args.fps:
    honorifics.time_utils.frame_rate = args.fps


lines = sys.stdin.readlines()

helper = SubStationFileHelper(lines)
event_dialogue = EventDialogueTiming(helper.event_format)

sys.stdout.write(''.join(lines[:helper.pos_start_dialogue]))

for index in range(helper.pos_start_dialogue, len(lines)):
    sys.stdout.write(event_dialogue.apply_timing_offset(lines[index]))
