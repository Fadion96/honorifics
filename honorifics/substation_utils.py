import re
from typing import Tuple, Any, Dict, Match
from collections import OrderedDict

from .time_utils import change_time


class EventDialogueTiming(object):
    dialogue_mark = 'Dialogue: '

    def __init__(self, event_format: Tuple[str]):
        self.format = event_format

        self.prog_timing_offset = re.compile(r' ?{([+-]\d+) (\w+)\}$')

    def __extract_dialogue(self, line: str) -> Dict[str, Any]:
        dialogue = OrderedDict()

        for index, field in enumerate(line[len(self.dialogue_mark):].split(',', len(self.format) - 1)):
            dialogue[self.format[index]] = field

        return dialogue

    def __dextract_dialogue(self, dialogue: Dict[str, Any]) -> str:
        return self.dialogue_mark + ','.join(dialogue.values())

    @staticmethod
    def __apply_timing_offset(match: Match[str], dialogue: Dict[str, Any]):
        (time, unit) = match.groups()

        time = int(time)

        if unit == 'frames':
            unit = 'frame'

        dialogue['Start'] = change_time(time, unit, dialogue['Start'], '.substation', '.substation')
        dialogue['End'] = change_time(time, unit, dialogue['End'], '.substation', '.substation')

        (begin, end) = match.span()

        dialogue['Text'] = dialogue['Text'][:begin] + (dialogue['Text'][end:] if end else '')

    def apply_timing_offset(self, line: str) -> str:
        if line.startswith(self.dialogue_mark):
            dialogue = self.__extract_dialogue(line)

            match = self.prog_timing_offset.search(dialogue['Text'])

            if match:
                self.__apply_timing_offset(match, dialogue)

                return self.__dextract_dialogue(dialogue)

        return line
