import unittest

import honorifics.time_utils as time_utils


class TestTimeUtils(unittest.TestCase):
    def test_change_time(self):
        result = time_utils.change_time(300, 'ms', '0:00:00.70', '.ass', '.ass')
        expected = '0:00:01.00'

        self.assertEqual(expected, result)
        pass
