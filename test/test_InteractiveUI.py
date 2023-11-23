import unittest
from unittest.mock import patch

import sys
sys.path.append("..")

from PIM.src.tools.InteractiveUI import InteractiveUI
import time

class TestInteractiveUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ui = InteractiveUI()

    def test_print_leave_message(self):
        self.ui.print_leave_message()
        time.sleep(0.5)  # Adding a small sleep to make sure outputs don't overlap

    def test_print_welcome_message(self):
        self.ui.print_welcome_message()
        time.sleep(0.5)

    def test_print_module_in(self):
        self.ui.print_module_in("Test Module")

    def test_print_module_out(self):
        self.ui.print_module_out("Test Module")

    @patch('builtins.input', side_effect=['5'])
    def test_get_int_input(self, mocked_input):
        # Here, the side_effect is set to ['5'], which means that the input function will return '5' when called.
        # Adjust this list based on the number of inputs you want to mock and their order.

        ui = InteractiveUI()
        result = ui.get_int_input(10)
        self.assertEqual(result, 5)

    def test_print_line(self):
        self.ui.print_line()

    def test_get_n_char(self):
        print(self.ui.get_n_char('a', 5), 'aaaaa')

    def test_print_choose_hint(self):
        self.ui.print_choose_hint("Test Name", "Test Description", "0-5")


if __name__ == "__main__":
    unittest.main()