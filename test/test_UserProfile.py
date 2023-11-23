import unittest
import sys
sys.path.append("..")
from PIM.src.model.user_profile import UserProfile

class UserProfileTests(unittest.TestCase):
    def setUp(self):
        self.user = UserProfile("John", "password123", "john@example.com", "User description")

    def tearDown(self):
        self.user = None

    def test_check_password(self):
        result = self.user.check_password("password123")
        self.assertTrue(result)

        result = self.user.check_password("wrongpassword")
        self.assertFalse(result)

    def test_set_password(self):
        self.user.set_password("newpassword")
        result = self.user.check_password("newpassword")
        self.assertTrue(result)

    def test_get_password(self):
        result = self.user.get_password()
        self.assertEqual(result, "password123")

    def test_get_name(self):
        result = self.user.get_name()
        self.assertEqual(result, "John")

    def test_str(self):
        expected_output = "Name: John\nEmail: john@example.com\nDescription: User description"
        result = str(self.user)
        self.assertEqual(result, expected_output)

    def test_eq(self):
        other_user = UserProfile("John", "password123")
        self.assertTrue(self.user == other_user)

        other_user = UserProfile("Jane", "password123")
        self.assertFalse(self.user == other_user)

        other_user = "John"
        self.assertFalse(self.user == other_user)

        other_user = UserProfile("John", "password123", "john@example.com", "User description")
        self.assertTrue(self.user == other_user)

        other_user = UserProfile("John", "password123", "different@example.com", "Different description")
        self.assertTrue(self.user == other_user)

        other_user = UserProfile("Jane", "password123", "john@example.com", "User description")
        self.assertFalse(self.user == other_user)

if __name__ == '__main__':
    unittest.main()