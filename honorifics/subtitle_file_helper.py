import re
from typing import Dict, List, Tuple


class AssFileHelper(object):
    def __init__(self, lines: List[str]):
        self.sections = {}
        self.dialogue_format = tuple()
        self.pos_start_dialogue = -1

        self.sections = self.__get_sections(lines)

        self.dialogue_format = self.__get_dialogue_format(lines)

        self.pos_start_dialogue = self.__get_first_dialogue_pos(lines)

    @staticmethod
    def __get_sections(lines: List[str], pattern=r'(?:\[).*(?:])') -> Dict[str, int]:
        result = {}

        prog = re.compile(pattern)
        for index, line in enumerate(lines):
            match_object = prog.match(line)
            if match_object:
                result[match_object.group(0)[1:-1]] = index

        return result

    def __get_dialogue_format(self, lines: List[str]) -> Tuple[str]:
        pos_format = self.sections['Events'] + 1

        return tuple(lines[pos_format][len('Format:'):].replace(' ', '').rstrip().split(','))

    def __get_first_dialogue_pos(self, lines):
        pos = self.sections['Events'] + 2

        while pos < len(lines):
            if lines[pos].startswith('Dialogue'):
                return pos

            pos += 1
        else:
            return -1
