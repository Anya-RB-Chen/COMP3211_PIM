import unittest
from unittest.mock import patch
from PIM.src.PIMApp import PIMApp
from PIM.src.MainPage import MainPage


class TestPIMApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.PIMApp = PIMApp()

    def test_login(self):
        # Test case for invalid name
        with unittest.mock.patch('builtins.input', side_effect=['Candy']):
            user_profile = self.PIMApp.login()
            self.assertIsNone(user_profile)

        # Test case for invalid password
        with unittest.mock.patch('builtins.input', side_effect=['Mike', '12345', '12345', '12345', '12345']):
            user_profile = self.PIMApp.login()
            self.assertIsNone(user_profile)

        # Test case for non-existent user
        with unittest.mock.patch('builtins.input', side_effect=['Mike', '123456']):
            user_profile = self.PIMApp.login()
            self.assertIsNotNone(user_profile)

    def test_register(self):
        # Test case for successful registration
        with unittest.mock.patch('builtins.input',
                                 side_effect=['Bruce', 'COMP3211ILoveYou%', '21099695d@connect.polyu.hk', 'PolyU']):
            user_profile = self.PIMApp.register()
            self.assertIsNotNone(user_profile)

        # Test case for invalid name
        with unittest.mock.patch('builtins.input', side_effect=['c', 'c', '0']):
            user_profile = self.PIMApp.register()
            self.assertIsNone(user_profile)

        # Test case for weak password
        with unittest.mock.patch('builtins.input',
                                 side_effect=['Leo1', '1', 'y', '21099695d@connect.polyu.hk', 'PolyU']):
            user_profile = self.PIMApp.register()
            self.assertIsNotNone(user_profile)

        # Test case for reset password
        with unittest.mock.patch('builtins.input',
                                 side_effect=['Leo2', '1', 'n', 'COMP3211ILoveYou%', '21099695d@connect.polyu.hk',
                                              'PolyU']):
            user_profile = self.PIMApp.register()
            self.assertIsNotNone(user_profile)

        # Test case for invalid email
        with unittest.mock.patch('builtins.input',
                                 side_effect=['Bruce2', 'COMP3211ILoveYou%', '123', '21099695d@connect.polyu.hk',
                                              'PolyU']):
            user_profile = self.PIMApp.register()
            self.assertIsNotNone(user_profile)

        # Test case for skipping email and description
        with unittest.mock.patch('builtins.input', side_effect=['Bruce3', 'COMP3211ILoveYou%', '0', '0']):
            user_profile = self.PIMApp.register()
            self.assertIsNotNone(user_profile)

    def test_main(self):
        # Test case for choice 1: log in system
        with patch('builtins.input', side_effect=['1', 'Mike', '123456']):
            with patch('builtins.print'):
                with patch.object(MainPage, 'main') as mock_main:
                    self.PIMApp.main()
                    mock_main.assert_called_once()

        # Test case for choice 2: register and log in directly
        with patch('builtins.input',
                   side_effect=['2', 'Max', '123456', 'y', '123456d@connect.polyu.hk', 'The lecturer of COMP3211',
                                '1']):
            with patch('builtins.print'):
                with patch.object(MainPage, 'main') as mock_main:
                    self.PIMApp.main()
                    mock_main.assert_called_once()


