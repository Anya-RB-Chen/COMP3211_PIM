import os
import traceback

from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.main_page import MainPage
import PIM.src.model
from PIM.src.model.system_manager import SystemManager, UserProfile
from PIM.src.tools.Tools import Tools
from PIM.src.model.user_manager import UserInformationManager


class PIMApp:
    """
    The first level displayed to each user. Users can choose to login or register.
    """
    # level 0
    def __init__(self):
        # file system initialization
        self.file_system_initialization()
        # System module initialization
        self.systemManager = SystemManager()

        self.mainPage = MainPage()

    # level 0:
    def main(self):
        """
        Main entry of the program.
        :return:
        """
        ui = InteractiveUI()
        # 1, welcome message and hint.
        ui.print_welcome_message()

        # 2. welcome page: log in system | register | quit
        choice = " \n1 --log in  2 --register 0-- quit"
        ui.print_choose_hint("", "", choice)

        choice = ui.get_int_input(2)
        # 3. choose to log / register/ quit
        try:
            if choice == 1:  # login
                userProfile = self.login()
                if userProfile:
                    self.mainPage.main(userProfile)
            elif choice == 2:  # register
                userProfile = self.register()
                if userProfile:
                    ui.print_choose_hint("", "Do you want to log in directly?", "1-- yes")
                    choice1 = ui.get_int_input(1)
                    if choice1:
                        self.mainPage.main(userProfile)
        except Exception:
            print("Error happens in welcome page.")
            traceback.print_exc()
            return -1

        # 4. print leave message
        ui.print_leave_message()

    # ------------------------------------------------------------------------------------------------------------------------------
    # level 1
    # file system initialization
    def file_system_initialization(self):
        # root folder initialization
        root_path = os.getcwd() + "/file"
        if not os.path.exists(root_path):
            os.mkdir(root_path)

        # system file initialization
        PIMApp.__systemFilePath = root_path + "/system.txt"

    def login(self):
        """
        Description: 1, ask the user to input name. (if enter 0, return None) 2, search name in the system. all of the
                    user profiles can be obtained by self.get_user_profiles() method (a list of UserProfile objects),
                     and the UserProfile object have "==" operator.  3, if the name not in the system,  return None.
                     otherwise, ask for enterring password (in UserProfile: check_password() -> bool ).
                     There are 3 chances at all. if the input is correct, return userProfile. otherwise, return None.
        :return: None
        """
        name = input("Please enter your name (enter 0 to quit): ").strip()
        if name == "0":
            return None
        user_profiles = self.systemManager.get_user_profiles()
        if user_profiles:
            for user_profile in user_profiles:
                if user_profile.get_name() == name:
                    for i in range(3):
                        password = input("Please enter your password: ").strip()
                        if user_profile.check_password(password):
                            return user_profile
                        print("wrong password. Sorry.")
                    return None
            print("Sorry, cannot find you in the system.")
        return None

    def register(self):
        """
    1,
    input: no
    output: quit -> return None,  |  successful -> return UserProfile, add valid user profile to system.

    (1) ask the user to enter the user name. use Tools.checkNameAvailable(name) to check whether the format of name is valid (define by yourself what is invalid format for name and implement this method with annotation to explain your standard)
    (2) search the user name in user profiles list (self.systemManager.get_user_profiles()) if the name already in system, give the hint to user and allow user to reenter a name.
    (3) ask the user to enter the password. check whether the password is strong enough by Tools.checkPasswordStrength(password) (the standard also defined by you, and implement the method with annotation)
        if the password is not strong, give the user hint to ask the user whether he want to keep the password or use new one. If he want to use new one, allow him to set the password again.
    (4) ask the user to add additional information: Email, and description, but this is optional.
    (5) create the UserProfile object for user and use g_SystemManager.add_profile() to add it into system
    (6) print the message "successfully register as new patron to the PIM system. Welcome !

    ps: In every round, there should have a hint (enter 0 to quit), if the user enter 0, return None
        """
        while True:
            # name
            name = input("Please enter your name (enter 0 to quit): ").strip()
            if name == "0":
                return None
            if not Tools.checkNameAvailable(name):
                print("Invalid name format. There are some requirements about the form of your user name:\n 1. "
                      "contains only letters, digits, and underscores;\n 2. starts with a letter;\n 3. has at least 3 "
                      "characters and at most 20 characters.\n Please input again.")
                continue
            user_profiles = self.systemManager.get_user_profiles()
            if user_profiles and UserProfile(name, "") in user_profiles:
                print("This name already exists. Please input again.")
                continue

            # password
            while True:
                password = input("Please enter your password (enter 0 to quit): ").strip()
                if password == "0":
                    return None
                if not Tools.checkPasswordStrength(password):
                    print("Weak password.\n Your password should ideally contain at least one uppercase letter, "
                          "one lowercase letter, one digit, and one special character.\n Do you still want to keep "
                          "it? (y/n)")
                    choice = input()
                    if choice.lower() == "n":
                        continue
                break

            # additional information
            email = input("Please enter your email (optional, enter 0 to skip): ")
            while email != "0" and not Tools.is_valid_email(email):
                email = input("Invalid Email. Please input again. (enter 0 to skip)")
            if email == "0":
                email = ""

            description = input("Please enter a description (optional, enter 0 to skip): ")
            if description == "0":
                description = ""

            # add to system.
            user_profile = UserProfile(name, password, email, description)
            self.systemManager.add_profile(user_profile)
            print("Successfully registered as a new patron to the PIM system. Welcome!")
            # ------------------------------------------------------------------------------------------------------------------------------
            self.systemManager.system_file_write()
            # ------------------------------------------------------------------------------------------------------------------------------

            return user_profile


if __name__ == "__main__":
    app = PIMApp()
    app.main()
