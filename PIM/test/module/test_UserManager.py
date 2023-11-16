import os
import unittest
from unittest.mock import MagicMock
from PIM.src.module.UserManager import UserIO


class TestUserIO(unittest.TestCase):
    def setUp(self):
        # Create a mock UserInformationManager object
        self.user_info_manager = MagicMock()
        self.user_info_manager.userName = "John"
        self.user_info_manager.get_PIM_List.return_value = ["PIM 1", "PIM 2", "PIM 3"]

        # Create an instance of UserIO
        self.user_io = UserIO(self.user_info_manager)

    def test_set_output_file_root_path(self):
        new_output_path = os.getcwd()+"/file/output.txt"
        self.user_io.set_output_file_root_path(new_output_path)
        self.assertEqual(self.user_io.get_output_file_root_path(), new_output_path)

    def test_output_user_information(self):
        file_name = "user_info"
        self.user_io.output_user_information(self.user_io.PIMList, file_name)

        # Verify that the file is created and contains the expected content
        expected_output = """\n             ☆──────────────✬❖✬───────────☆
             │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
             │       😄   PERSONAL  😃     │
             │       😆 INFORMATION 😁     │
             │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
             ☆──────────────✬❖✬───────────☆

            \n\nHi John, You have 3 personal information records.\n\n\nPIM 1: \nPIM 1\n\nPIM 2: \nPIM 2\n\nPIM 3: \nPIM 3\n"""

        with open(f"./file/output/John/{file_name}.pim", "r", encoding="utf-8") as f:
            actual_output = f.read()

        self.assertEqual(actual_output, expected_output)

    def test_output_specified_information(self):
        file_name = "specified_info"
        choices = [1, 2]
        self.user_io.output_specified_information(self.user_io.PIMList, choices, file_name)

        # Verify that the file is created and contains the expected content
        expected_output = """\n                       ──────────────✬❖✬───────────
                     │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
                     │       😄   PERSONAL  😃     │
                     │       😆 INFORMATION 😁     │
                     │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
                       ──────────────✬❖✬───────────

                    \n\nHi John! Here are 2 personal information records that you selected.\n\n\nPIM 1: \nPIM 1\n\nPIM 2: \nPIM 2\n"""

        with open(f"./file/output/John/{file_name}.pim", "r", encoding="utf-8") as f:
            actual_output = f.read()
        self.maxDiff = 10000
        self.assertEqual(actual_output, expected_output)

    def test_load_file(self):
        file_name = "user_info"
        expected_output = "File contents"

        # Create a mock for the file
        file_mock = MagicMock()
        file_mock.__enter__.return_value.read.return_value = expected_output

        # Mock the open() function and patch it to return the file_mock
        with unittest.mock.patch('builtins.open', return_value=file_mock):
            with unittest.mock.patch('builtins.print') as mock_print:
                self.user_io.load_file(file_name)
                mock_print.assert_called_with(expected_output)

    def tearDown(self):
        # Clean up any files created during the tests
        file_path1 = "./file/output/John/user_info.pim"
        file_path2 = "./file/output/John/specified_info.pim"

        # Remove the test files if they exist
        if os.path.exists(file_path1):
            os.remove(file_path1)
        if os.path.exists(file_path2):
            os.remove(file_path2)


if __name__ == "__main__":
    unittest.main()