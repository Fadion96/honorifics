import re
from typing import Dict, List, Tuple


class SubStationFileHelper(object):
    def __init__(self, lines: List[str]):
        self.sections = self.__get_sections(lines)

        self.event_format, self.pos_event_format = self.__get_event_format(lines)

        self.pos_start_dialogue = self.__pos_startswith_in_lines('Dialogue', lines, self.pos_event_format + 1)

    @staticmethod
    def __get_sections(lines: List[str]) -> Dict[str, int]:
        result = {}

        prog = re.compile(r'(?:\[)(.*)(?:])')
        for index, line in enumerate(lines):
            match_object = prog.match(line)
            if match_object:
                result[match_object.group(1)] = index

        return result

    @staticmethod
    def __pos_startswith_in_lines(text: str, lines: List[str], pos: int = 0) -> int:
        while pos < len(lines):
            if lines[pos].startswith(text):
                return pos

            pos += 1
        else:
            return -1

    def __get_event_format(self, lines: List[str]) -> (Tuple[str], int):
        pos = self.__pos_startswith_in_lines('Format', lines, self.sections['Events'] + 1)

        return tuple(lines[pos][len('Format:'):].replace(' ', '').rstrip().split(',')), pos
