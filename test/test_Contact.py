import unittest
import sys
sys.path.append("..")
from PIM.src.model.contact import Contact


class ContactTests(unittest.TestCase):
    def setUp(self):
        self.contact = Contact.create("John Doe", {"mobile_number": "1234567890", "address": "123 Elm St"})

    def test_create(self):
        fields_map = {
            "mobile_number": "9876543210",
            "address": "456 Elm St"
        }
        contact = Contact.create("Jane Smith", fields_map)
        self.assertEqual(contact.name, "Jane Smith")
        self.assertEqual(contact.mobile_number, "9876543210")
        self.assertEqual(contact.address, "456 Elm St")

    def test_get_fields(self):
        fields = Contact.get_fields()
        expected_fields = ["name", "mobile_number", "address"]
        self.assertEqual(fields, expected_fields)

    def test_get_explanation(self):
        explanation = Contact.get_explanation()
        expected_explanation = "A contact is a person's information, including name, mobile numbers, and address."
        self.assertEqual(explanation, expected_explanation)

    def test_get_fields_contents_map(self):
        contents_map = self.contact.get_fields_contents_map()
        expected_map = {
            "name": "John Doe",
            "mobile_number": "1234567890",
            "address": "123 Elm St"
        }
        self.assertEqual(contents_map, expected_map)

    def test_get_fields_checkers_map(self):
        checkers_map = Contact.get_fields_checkers_map()
        self.assertTrue(callable(checkers_map["name"]))
        self.assertTrue(callable(checkers_map["mobile_number"]))
        self.assertTrue(callable(checkers_map["address"]))

    def test_contain_text(self):
        self.assertTrue(self.contact.contain_text("John"))
        self.assertTrue(self.contact.contain_text("1234567890"))
        self.assertTrue(self.contact.contain_text("Elm St"))
        self.assertFalse(self.contact.contain_text("Jane"))

    def test_str(self):
        expected_str = "Name: John Doe\nType: Contact\nMobile number: 1234567890\nAddress: 123 Elm St"
        self.assertEqual(str(self.contact), expected_str)

    def test_time_condition_checker(self):
        self.assertFalse(self.contact.time_condition_checker(10.0, ">"))
        self.assertFalse(self.contact.time_condition_checker(10.0, "<"))
        self.assertFalse(self.contact.time_condition_checker(10.0, "=="))

    def test_get_field_checker(self):
        name_checker = Contact.get_field_checker("name")
        self.assertTrue(callable(name_checker))

    def test_create_object_from_lines(self):
        lines = [
            "Name: John Doe\n",
            "Type: Contact\n",
            "Mobile number: 1234567890\n",
            "Address: 123 Elm St\n"
        ]
        index = 0
        contact = Contact.create_object_from_lines(lines, index)
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.mobile_number, "1234567890")
        self.assertEqual(contact.address, "123 Elm St")


if __name__ == "__main__":
    unittest.main()