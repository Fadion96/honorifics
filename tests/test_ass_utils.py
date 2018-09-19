import unittest

from honorifics.ass_utils import EventDialogueLineTiming


class TestEventDialogueLineTiming(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dialogue_line_timing = EventDialogueLineTiming(tuple(['Start', 'End', 'Text']))

    def test_apply_timing_offset(self):
        self.assertEqual('Dialogue: 0:01:01.01,0:59:58.99, Text',
                         self.dialogue_line_timing.apply_timing_offset('Dialogue: 0:01:02.02,1:00:00.00, Text {-101 cs}'))
        #  5 frames with 23.976 fps ~ floor(20,8) cs
        self.assertEqual('Dialogue: 1:00:00.20,1:00:11.10, Text',
                         self.dialogue_line_timing.apply_timing_offset('Dialogue: 1:00:00.00,1:00:10.90, Text {+5 frames}'))

    def test_ignore_normal_line(self):
        self.assertEqual('Dialogue: 0:01:01.01,0:59:58.99, Text ',
                         self.dialogue_line_timing.apply_timing_offset('Dialogue: 0:01:01.01,0:59:58.99, Text '))
