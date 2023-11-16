import os


# 单例模式 + 全局变量解决访问问题。  （类方法无法整合字段，失去变相对象意义； 不用全局变量传递对象不方便）
g_SystemManager = None


# 理想方式： 在原有文本上改动，支持多线程同时访问，且能够处理死锁。
# naive方式： 单进程访问，直接重新写所有内容。 只需要定义encoding、decoding方法， 其他处理完全基于对象
class SystemManager:  # 老子不用file manager了，直接封装在系统内，毕竟解码方式和相关

    __instance = None

    def __init__(self):
        # singleton
        if not SystemManager.__instance:
            # self.__filePath = filePath
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
        self.__systemFileManager.write()

    def get_user_profiles(self):
        return self.__user_profiles.copy()

    def add_profile(self, userProfile):
        if userProfile:
            self.__user_profiles.append(userProfile)




class UserProfile:
    # __count = 0

    def __init__(self, name, password, email="", description=""):
        # self.id = UserProfile.__count
        # UserProfile.__count += 1

        self.__name = name
        self.__password = password
        self.__email = email
        self.__description = description

    def check_password(self, password):
        return self.__password == password

    def set_password(self, new_password):
        self.__password = new_password

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def __str__(self):
        return f"Name: {self.__name}\nEmail: {self.__email}\nDescription: {self.__description}"

    def __eq__(self, other):
        return isinstance(other, UserProfile) and self.get_name() == other.get_name()



class SystemFileManager:

    def __init__(self, systemFilePath):
        self.__systemFilePath = systemFilePath
        if not os.path.exists(systemFilePath):
            self.create()
        self.__user_profiles = self.read()


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

    def write(self):
        with open (self.__systemFilePath, "w") as f:
            f.write("User Profiles:\n\n")
            for userProfile in self.__user_profiles:
                name = userProfile.get_name()
                password = userProfile.get_password()
                f.write("name:" + name + "\n")
                f.write("password:" + password + "\n")
                f.write("\n")


