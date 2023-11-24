import os
import sys
sys.path.append("../..")
from model.user_profile import UserProfile
from model import *

class SystemFileManager:

    def __init__(self, systemFilePath):
        self.__systemFilePath = systemFilePath
        if not os.path.exists(systemFilePath):
            self.create()
        # self.__user_profiles = self.read()


    def create(self):
        if not os.path.exists(self.__systemFilePath):
            with open(self.__systemFilePath, "w") as f:
                f.write("")

    def read(self) -> list:
        with open(self.__systemFilePath, "r") as f:
            lines = f.readlines()
            index = 2
            user_profiles = []
            while index < len(lines):
                line = lines[index]
                if line == "\n":
                    index += 1
                    continue

                if line.startswith("name:"):
                    name = line[len("name:"):].strip()
                    password = lines[index + 1][len("password:"):].strip()
                    user_profiles.append(UserProfile(name, password))
                    index += 2
                else:
                    index += 1

            return user_profiles

    def write(self,userProfiles):
        with open (self.__systemFilePath, "w") as f:
            f.write("User Profiles:\n\n")
            for userProfile in userProfiles:
                name = userProfile.get_name()
                password = userProfile.get_password()
                f.write("name:" + name + "\n")
                f.write("password:" + password + "\n")
                f.write("\n")


