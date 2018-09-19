import re
from typing import Tuple, Any, Dict, Match
from collections import OrderedDict

from .time_utils import change_time


class EventDialogueLineTiming(object):
    dialogue_mark: str = 'Dialogue: '

    def __init__(self, dialogue_format: Tuple[str], pattern_timing_offset: str = r' ?{([+-]\d+) (\w+)\}$'):
        self.format = dialogue_format

        self.pattern_timing_offset = re.compile(pattern_timing_offset)

    def __extract_dialogue(self, line: str) -> Dict[str, Any]:
        dialogue = OrderedDict()

        for index, field in enumerate(line[len(self.dialogue_mark):].split(',', 9)):
            dialogue[self.format[index]] = field

        return dialogue

    def __dextract_dialogue(self, dialogue: Dict[str, Any]) -> str:
        return self.dialogue_mark + ','.join(dialogue.values())

    @staticmethod
    def __apply_timing_offset(match: Match[str], line_length: int, dialogue: Dict[str, Any]):
        (time, unit) = match.groups()

        time = int(time)

        if unit == 'frames':
            unit = 'frame'

        dialogue['Start'] = change_time(time, unit, dialogue['Start'], '.ass', '.ass')
        dialogue['End'] = change_time(time, unit, dialogue['End'], '.ass', '.ass')

        (begin, end) = match.span()

        begin -= line_length
        end -= line_length

        dialogue['Text'] = dialogue['Text'][:begin] + (dialogue['Text'][end:] if end else '')

    def apply_timing_offset(self, line: str) -> str:
        match = self.pattern_timing_offset.search(line)

        if match:
            dialogue = self.__extract_dialogue(line)

            self.__apply_timing_offset(match, len(line), dialogue)

            return self.__dextract_dialogue(dialogue)
        else:
            return line
