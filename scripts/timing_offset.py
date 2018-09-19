#!/usr/bin/env python3
import sys
sys.path.insert(0, '../')

from honorifics.subtitle_file_helper import AssFileHelper
from honorifics.ass_utils import EventDialogueLineTiming


lines = sys.stdin.readlines()

ass_helper = AssFileHelper(lines)
dialogue_line = EventDialogueLineTiming(ass_helper.dialogue_format)

sys.stdout.write(''.join(lines[:ass_helper.pos_start_dialogue]))

for index in range(ass_helper.pos_start_dialogue, len(lines)):
    sys.stdout.write(dialogue_line.apply_timing_offset(lines[index]))
