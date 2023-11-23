import unittest
from unittest.mock import patch
import sys
sys.path.append("..")
from PIM.src.model.system_manager import SystemManager



class SystemManagerTests(unittest.TestCase):
    def setUp(self):
        self.system_manager = SystemManager()

    def tearDown(self):
        self.system_manager = None

    def test_system_file_read(self):
        # Mocking the SystemFileManager's read method
        with patch.object(self.system_manager._SystemManager__systemFileManager, 'read') as mock_read:
            mock_read.return_value = ['user1', 'user2']
            result = self.system_manager.system_file_read()
            self.assertEqual(result, ['user1', 'user2'])

    def test_system_file_write(self):
        # Mocking the SystemFileManager's write method
        with patch.object(self.system_manager._SystemManager__systemFileManager, 'write') as mock_write:
            self.system_manager.system_file_write()
            mock_write.assert_called_with(self.system_manager._SystemManager__user_profiles)

    def test_get_user_profiles(self):
        self.system_manager._SystemManager__user_profiles = ['user1', 'user2']
        result = self.system_manager.get_user_profiles()
        self.assertEqual(result, ['user1', 'user2'])

    def test_add_profile(self):
        self.system_manager._SystemManager__user_profiles = ['user1']
        self.system_manager.add_profile('user2')
        self.assertEqual(self.system_manager._SystemManager__user_profiles, ['user1', 'user2'])


if __name__ == '__main__':
    unittest.main()