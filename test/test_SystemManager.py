import unittest
import os
import sys
sys.path.append("..")
from PIM.src.model.system_manager import SystemManager, SystemFileManager, UserProfile

"""把测试文件全部放到test/testfile中"""

class SystemManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = SystemManager()

    def tearDown(self):
        # Clean up any files created during the tests
        system_file_path = os.getcwd() + "/file" + "/.system.txt"
        if os.path.exists(system_file_path):
            os.remove(system_file_path)

    def test_add_profile(self):
        profile = UserProfile("Alice", "password123")
        self.manager.add_profile(profile)

        user_profiles = self.manager.get_user_profiles()
        self.assertEqual(len(user_profiles), 1)
        self.assertEqual(user_profiles[0], profile)

    def test_system_file_read_write(self):
        profile1 = UserProfile("Alice", "password123")
        profile2 = UserProfile("Bob", "pass123")
        self.manager.add_profile(profile1)
        self.manager.add_profile(profile2)

        self.manager.system_file_write()

        # Create a new SystemManager instance to simulate program restart
        new_manager = SystemManager()

        # Read user profiles from the system file
        user_profiles = new_manager.system_file_read()

        self.assertEqual(len(user_profiles), 2)
        self.assertIn(profile1, user_profiles)
        self.assertIn(profile2, user_profiles)


class SystemFileManagerTests(unittest.TestCase):
    def setUp(self):
        system_file_path = os.getcwd() + "/file" + "/.system.txt"
        self.file_manager = SystemFileManager(system_file_path)

    def tearDown(self):
        # Clean up any files created during the tests
        system_file_path = os.getcwd() + "/file" + "/.system.txt"
        if os.path.exists(system_file_path):
            os.remove(system_file_path)

    def test_read_write(self):
        profile1 = UserProfile("Alice", "password123")
        profile2 = UserProfile("Bob", "pass123")

        user_profiles = [profile1, profile2]

        # Write user profiles to the system file
        self.file_manager.write(user_profiles)

        # Read user profiles from the system file
        read_profiles = self.file_manager.read()

        self.assertEqual(len(read_profiles), 2)
        self.assertIn(profile1, read_profiles)
        self.assertIn(profile2, read_profiles)


if __name__ == "__main__":
    unittest.main()