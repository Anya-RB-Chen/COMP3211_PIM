import unittest
import os
from PIM.src.module.SystemManager import SystemManager, SystemFileManager, UserProfile

"""把测试文件全部放到test/testfile中"""

class TestSystemManager(unittest.TestCase):

    def setUp(self):
        self.system_manager = SystemManager()

    def test_system_file_read(self):
        # Test when the system file is empty
        expected_output = []
        self.assertEqual(self.system_manager.system_file_read(), expected_output)

    def test_system_file_write(self):
        # Test if the system file is written successfully
        self.system_manager.add_profile(UserProfile("John", "password123"))
        self.system_manager.add_profile(UserProfile("Alice", "pass456"))
        self.system_manager.system_file_write()
        # Check if the file is created and not empty
        system_path = os.getcwd() + "/file/.system.txt"
        with open(system_path, "r") as f:
            content = f.read()
            self.assertTrue(content)

    def test_get_user_profiles(self):
        # Test when there are user profiles
        self.system_manager.add_profile(UserProfile("John", "password123"))
        self.system_manager.add_profile(UserProfile("Alice", "pass456"))
        expected_output = [UserProfile("John", "password123"), UserProfile("Alice", "pass456")]
        self.assertEqual(self.system_manager.get_user_profiles(), expected_output)

    def test_add_profile(self):
        # Test if the profile is added successfully
        self.system_manager.add_profile(UserProfile("John", "password123"))
        self.system_manager.add_profile(UserProfile("Alice", "pass456"))
        expected_output = [UserProfile("John", "password123"), UserProfile("Alice", "pass456")]
        self.assertEqual(self.system_manager.get_user_profiles(), expected_output)


class TestSystemFileManager(unittest.TestCase):

    def setUp(self):
        self.system_file_path = os.getcwd() + "/file/.test_system_file.txt"
        self.system_file_manager = SystemFileManager(self.system_file_path)

    def tearDown(self):
        # Remove the test system file after the test
        os.remove(self.system_file_path)

    def test_create(self):
        # Test if the system file is created successfully
        self.system_file_manager.create()
        self.assertTrue(os.path.exists(self.system_file_path))

    def test_read(self):
        # Test when the system file is empty
        expected_output = []
        self.assertEqual(self.system_file_manager.read(), expected_output)

        # Test when the system file contains user profiles
        with open(self.system_file_path, "w") as f:
            f.write("User Profiles:\n\n")
            f.write("name: John\n")
            f.write("password: password123\n")
            f.write("\n")
            f.write("name: Alice\n")
            f.write("password: pass456\n")
            f.write("\n")

        expected_output = [UserProfile("John", "password123"), UserProfile("Alice", "pass456")]
        self.assertEqual(self.system_file_manager.read(), expected_output)

    def test_write(self):
        # Test if the user profiles are written successfully to the system file
        self.system_file_manager._SystemFileManager__user_profiles = [
            UserProfile("John", "password123"),
            UserProfile("Alice", "pass456")
        ]
        self.system_file_manager.write()
        # Check if the file is created and not empty
        with open(self.system_file_path, "r") as f:
            content = f.read()
            self.assertTrue(content)


if __name__ == '__main__':
    unittest.main()