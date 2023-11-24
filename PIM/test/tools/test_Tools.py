import unittest
from PIM.src.tools.Tools import *


class TestTools(unittest.TestCase):

    def test_checkNameAvailable(self):
        self.assertTrue(Tools.checkNameAvailable("valid_name"))
        self.assertTrue(Tools.checkNameAvailable("valid_name_123"))
        self.assertFalse(Tools.checkNameAvailable("invalid name"))
        self.assertFalse(Tools.checkNameAvailable("ab"))
        self.assertFalse(Tools.checkNameAvailable("very_long_name_that_exceeds_the_character_limit"))

    def test_checkPasswordStrength(self):
        self.assertTrue(Tools.checkPasswordStrength("StrongPass123!"))
        self.assertFalse(Tools.checkPasswordStrength("weakpass"))
        self.assertFalse(Tools.checkPasswordStrength("no_digit_or_special_char"))
        self.assertFalse(Tools.checkPasswordStrength("NoSpecialChar123"))
        self.assertFalse(Tools.checkPasswordStrength("OnlyLowerCaseletters"))

    def test_is_valid_email(self):
        self.assertTrue(Tools.is_valid_email("example.email@domain.com"))
        self.assertFalse(Tools.is_valid_email("invalid_email@domain"))
        self.assertFalse(Tools.is_valid_email("another.invalid_email@.com"))

    def test_check_time_format(self):
        self.assertEqual(Tools.check_time_format("2023-10-18 14:00"), "")
        self.assertEqual(Tools.check_time_format("2023-10-18 14:00:00"),
                         "Expected format: YYYY-MM-DD HH:MM, e.g., 2023-10-18 14:00")
        self.assertEqual(Tools.check_time_format("2023/10/18 14:00"),
                         "Expected format: YYYY-MM-DD HH:MM, e.g., 2023-10-18 14:00")

    def test_check_comparator_format(self):
        self.assertEqual(Tools.check_comparator_format("<"), "")
        self.assertEqual(Tools.check_comparator_format("="), "")
        self.assertEqual(Tools.check_comparator_format(">"), "")
        self.assertEqual(Tools.check_comparator_format("!"), "Expected one of the following comparators: <, =, >")

    def test_check_PIM_type_format(self):
        self.assertEqual(Tools.check_PIM_type_format("task"), "")
        self.assertEqual(Tools.check_PIM_type_format("plaintext"), "")
        self.assertEqual(Tools.check_PIM_type_format("event"), "")
        self.assertEqual(Tools.check_PIM_type_format("contact"), "")
        self.assertEqual(Tools.check_PIM_type_format("invalid_type"),
                         "Expected one of the following PIM types: Task, PlainText, Event, Contact")

    def test_check_email_format(self):
        self.assertEqual(Tools.check_email_format("example@example.com"), "")
        self.assertEqual(Tools.check_email_format("invalid_email"),
                         "Invalid format. Expected a valid email format, e.g., example@example.com")

    def test_check_mobile_number_format(self):
        self.assertEqual(Tools.check_mobile_number_format("123-456-7890"), "")
        self.assertEqual(Tools.check_mobile_number_format("1234567890"), "")
        self.assertEqual(Tools.check_mobile_number_format("123-456"),
                         "Mobile numbers should only contain digits and be in the format '123-456-7890'.")

    def test_get_type_format_checker(self):
        self.assertEqual(Tools.get_type_format_checker(InputType.COMPARATOR), Tools.check_comparator_format)
        self.assertEqual(Tools.get_type_format_checker(InputType.TIME), Tools.check_time_format)
        self.assertEqual(Tools.get_type_format_checker(InputType.EMAIL), Tools.check_email_format)
        self.assertEqual(Tools.get_type_format_checker(InputType.PIMTYPE), Tools.check_PIM_type_format)
        self.assertIsNone(Tools.get_type_format_checker("invalid_type"))

    def test_timeStr_to_timeStamp(self):
        dt = datetime.strptime("2023-10-18 14:00", "%Y-%m-%d %H:%M").timestamp()
        self.assertEqual(int(Tools.timeStr_to_timeStamp("2023-10-18 14:00")), dt)

    def test_timeStamp_to_timeStr(self):
        dt = datetime.utcfromtimestamp(1670463600).strftime("%Y-%m-%d %H:%M")
        self.assertEqual(Tools.timeStamp_to_timeStr(1670463600), dt)

    def test_get_value_from_line(self):
        line = "Key: Value"
        self.assertEqual(Tools.get_value_from_line(line), "Value")


if __name__ == '__main__':
    unittest.main()