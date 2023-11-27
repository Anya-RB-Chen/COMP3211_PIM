import os
from PIM.src.file_manager.system_file_manager import SystemFileManager
from PIM.src.model.user_profile import UserProfile

g_SystemManager = None


class SystemManager:
    """
    This is the system manager class. It manages the system file which stores user login information
    """

    __instance = None

    def __init__(self):
        # singleton
        if not SystemManager.__instance:
            SystemManager.__instance = self

        # write buffer initialization.
        self.__history = []  # str
        systemFilePath = os.getcwd() + "/file" + "/.system.txt"
        self.__systemFileManager = SystemFileManager(systemFilePath)

        self.__user_profiles = self.__systemFileManager.read()  # profile object
        if not self.__user_profiles:
            self.__user_profiles = []
        self.__system_state = []

        global g_SystemManager
        g_SystemManager = self


    def check_username_form(self, name):
        while True:
            if len(name) > 10:
                print("Sorry, your username must be less than 20 characters long.")

    def system_file_read(self) -> list:
        return self.__systemFileManager.read()

    def system_file_write(self):
        self.__systemFileManager.write(self.__user_profiles)

    def get_user_profiles(self):
        return self.__user_profiles.copy()

    def add_profile(self, userProfile):
        if userProfile:
            self.__user_profiles.append(userProfile)





