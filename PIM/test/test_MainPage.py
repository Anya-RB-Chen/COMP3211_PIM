import unittest
from unittest.mock import patch
from PIM.src.main_page import MainPage
from PIM.src.model.contact import Contact
from PIM.src.model.task import Task
from PIM.src.model.system_manager import SystemManager
from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.model.user_manager import UserInformationManager as User
import os


class TestMainPage(unittest.TestCase):
    def setUp(self):
        defaultUserProfile = SystemManager().get_user_profiles()[0]
        self.main_page = MainPage()
        self.main_page.ui = InteractiveUI()
        self.main_page._userManager = User(defaultUserProfile)

    def test_create_new_PIM_save(self):
        with patch('builtins.input', side_effect=['4', 'Attend meeting', 'Team sync-up', '2023-11-21 09:00', '2023-11-21 08:00', '1']):
            self.main_page.create_new_PIM()
            self.assertEqual(len(self.main_page._userManager.get_PIM_List()), 11)

        #self.main_page._userManager.add_PIM.assert_called()

    def test_create_new_PIM_quit(self):
        with patch('builtins.input', side_effect=['4', 'Attend meeting', 'Team sync-up', '2023-11-21 09:00', '', '0']):
            self.main_page.create_new_PIM()
        #self.main_page._userManager.add_PIM.assert_called()

    def test_manipulate_existing_PIM_delete_searchType(self):
        # Test deleting a PIM
        # pim = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        # self.main_page._userManager.add_PIM(pim)

        #mock_input.side_effect = ['1', 'Contact', "delete 3"]
        with patch('builtins.input', side_effect=['1', 'Contact',"delete 2", "0"]):
            self.main_page.manipulate_existing_PIM()

        # pim_list = self.main_page._userManager.get_PIM_List()
        # self.assertNotIn(pim, pim_list)
    def test_manipulate_existing_PIM_delete_searchText(self):
        with patch('builtins.input', side_effect=['2', 'a', "delete 2", "0"]):
            self.main_page.manipulate_existing_PIM()

    def test_manipulate_existing_PIM_delete_cannotFind(self):
        with patch('builtins.input', side_effect=['2', '<', "2023-11-20 12:00", "delete 2", "0"]):
            self.main_page.manipulate_existing_PIM()

    def test_manipulate_existing_PIM_delete_searchTime(self):
        with patch('builtins.input', side_effect=['3', '>', "2023-11-20 12:00", "delete 1", "0"]):
            self.main_page.manipulate_existing_PIM()

    def test_manipulate_existing_PIM_delete_searchCompound1(self):
        with patch('builtins.input', side_effect=['4', "type: Task &&  text: ! a || time: < 2023-10-18 14:00", "delete 1", "0"]):
            self.main_page.manipulate_existing_PIM()

    def test_manipulate_existing_PIM_delete_searchCompound2(self):
        with patch('builtins.input', side_effect=['4', "type: Contact &&  text: ! a && time: > 2023-10-18 14:00", "delete 1", "0"]):
            self.main_page.manipulate_existing_PIM()

    def test_manipulate_existing_PIM_delete_searchCompoundFalse(self):
        with patch('builtins.input', side_effect=['4', "type: Contact &&  text: !a && time: > 2023-10-18 14:00", "delete 1", "0"]):
            self.main_page.manipulate_existing_PIM()

    def test_manipulate_existing_PIM_delete_true(self):
        with patch('builtins.input', side_effect=['4', 'Attend meeting', 'Team sync-up', '2023-11-21 09:00', '2023-11-21 08:00', '1']):
            self.main_page.create_new_PIM()
        with patch('builtins.input', side_effect=['1', 'task', "delete 2", "1"]):
            self.main_page.manipulate_existing_PIM()
            self.assertEqual(len(self.main_page._userManager.get_PIM_List()), 10)

    def test_manipulate_existing_PIM_modify(self):
        # Test modifying a PIM
        pim = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        self.main_page._userManager.add_PIM(pim)

        with patch('builtins.input', side_effect=['1', 'task', 'modify 1', '1', 'Buy Groceries', '0']):
            self.main_page.manipulate_existing_PIM()

        self.assertEqual(pim.name, "John Doe")

    def test_generate_personal_PIM_report(self):
        # Test generating a report
        pim1 = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        pim2 = Task.create("Buy groceries", {"description": "Buy milk, bread, and eggs", "deadline": "2023-10-25 09:00"})
        self.main_page._userManager.add_PIM(pim1)
        self.main_page._userManager.add_PIM(pim2)

        with patch('builtins.input', side_effect=['1', '0', 'sample']):
            self.main_page.generate_personal_PIM_report()
            self.assertTrue(os.path.exists('file/output/Mike/sample.pim'))

    def test_load_PIM_file(self):
        # Test loading a file
        with patch('builtins.input', side_effect=['sample']):
            self.main_page.load_PIM_file()
            self.assertEqual(len(self.main_page._userManager.get_PIM_List()), 11)

    def test_main(self):
        with patch('builtins.input', side_effect=['1', '4', 'Attend meeting', 'Team sync-up', '2023-11-21 09:00', '2023-11-21 08:00', '0', '0']):
            self.main_page.main(SystemManager().get_user_profiles()[0])


