import unittest

from honorifics.subtitle_file_helper import SubStationFileHelper


class TestSubStationFileHelper(unittest.TestCase):
    def test_variables(self):
        data = [
            '',
            '[Events]',
            'Format: Time, Text',
            '',
            'Dialogue: 0:00:00.0, Test'
        ]

        helper = SubStationFileHelper(data)
        self.assertEqual({'Events': 1}, helper.sections)
        self.assertEqual(('Time', 'Text'), helper.event_format)
        self.assertEqual(2, helper.pos_event_format)
        self.assertEqual(4, helper.pos_start_dialogue)
