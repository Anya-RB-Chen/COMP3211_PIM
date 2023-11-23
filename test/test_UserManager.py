import unittest
import sys
sys.path.append("..")
from PIM.src.model.user_manager import UserInformationManager
from PIM.src.model.user_profile import UserProfile
from PIM.src.model.contact import Contact
from PIM.src.model.event import Event
from PIM.src.model.task import Task
from PIM.src.model.plain_text import PlainText


class UserInformationManagerTests(unittest.TestCase):
    def setUp(self):
        user_profile = UserProfile("John","123456")
        self.user_information_manager = UserInformationManager(user_profile)

    def tearDown(self):
        self.user_information_manager = None

    def test_get_PIM_List(self):
        pim_list = []
        self.user_information_manager._UserInformationManager__PIMList = pim_list
        result = self.user_information_manager.get_PIM_List()
        self.assertEqual(result, pim_list)

    def test_add_PIM(self):
        pim = Contact.create("John Doe", {"mobile_number": "1234567890", "address": "123 Elm St"})
        result = self.user_information_manager.add_PIM(pim)
        self.assertTrue(result)
        self.assertIn(pim, self.user_information_manager._UserInformationManager__PIMList)

    def test_contains_name(self):
        pim = Contact.create("John Doe", {"mobile_number": "1234567890", "address": "123 Elm St"})
        self.user_information_manager._UserInformationManager__PIMList = [pim]
        result = self.user_information_manager.contains_name("John Doe")
        self.assertTrue(result)

    def test_search_name(self):
        pim = Contact.create("John Doe", {"mobile_number": "1234567890", "address": "123 Elm St"})
        self.user_information_manager._UserInformationManager__PIMList = [pim]
        result, index = self.user_information_manager.search_name("John Doe")
        self.assertEqual(result, pim)
        self.assertEqual(index, 0)

        pim = Contact.create("John Doe", {"mobile_number": "1234567890", "address": "123 Elm St"})
        new_pim = Contact.create("John Doe", {"mobile_number": "1234567890", "address": "123 Elm St"})
        self.user_information_manager._UserInformationManager__PIMList = [pim]
        result = self.user_information_manager.modify(pim, new_pim)
        self.assertTrue(result)
        self.assertIn(new_pim, self.user_information_manager._UserInformationManager__PIMList)

    def test_delete(self):
        pim = Contact.create("John Doe", {"mobile_number": "1234567890", "address": "123 Elm St"})
        self.user_information_manager._UserInformationManager__PIMList = [pim]
        result = self.user_information_manager.delete(pim)
        self.assertTrue(result)
        self.assertNotIn(pim, self.user_information_manager._UserInformationManager__PIMList)

    def test_get_PIMClassList(self):
        pim_class_list = [Contact, Event, PlainText, Task]
        result = self.user_information_manager.get_PIMClassList()
        self.assertEqual(result, pim_class_list)

    def test_PIM_type_to_class(self):
        result = self.user_information_manager.PIM_type_to_class("contact")
        self.assertEqual(result, Contact)
        result = self.user_information_manager.PIM_type_to_class("event")
        self.assertEqual(result, Event)
        result = self.user_information_manager.PIM_type_to_class("plaintext")
        self.assertEqual(result, PlainText)
        result = self.user_information_manager.PIM_type_to_class("task")
        self.assertEqual(result, Task)
        result = self.user_information_manager.PIM_type_to_class("invalid_type")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()