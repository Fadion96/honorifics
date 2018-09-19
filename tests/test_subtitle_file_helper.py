import unittest
from typing import List

from honorifics.subtitle_file_helper import AssFileHelper


class TestAssFileHelper(unittest.TestCase):
    def test_variables(self):
        data: List[str] = [
            '',
            '[Events]',
            'Format: Time, Text',
            '',
            'Dialogue: 0:00:00.0, Test'
        ]

        helper = AssFileHelper(data)
        self.assertEqual({'Events': 1}, helper.sections)
        self.assertEqual(('Time', 'Text'), helper.dialogue_format)
        self.assertEqual(4, helper.pos_start_dialogue)
