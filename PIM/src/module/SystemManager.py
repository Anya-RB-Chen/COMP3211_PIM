import os


# 单例模式 + 全局变量解决访问问题。  （类方法无法整合字段，失去变相对象意义； 不用全局变量传递对象不方便）
g_SystemManager = None


# 理想方式： 在原有文本上改动，支持多线程同时访问，且能够处理死锁。
# naive方式： 单进程访问，直接重新写所有内容。 只需要定义encoding、decoding方法， 其他处理完全基于对象
class SystemManager:  # 老子不用file manager了，直接封装在系统内，毕竟解码方式和相关

    __instance = None

    def __init__(self, filePath):
        # singleton
        if not SystemManager.__instance:
            self.__filePath = filePath

            if not os.path.exists(filePath):
                self.system_file_create()

            # write buffer initialization.
            self.__history = []  # str
            self.__user_profiles = []  # profile object
            self.__system_state = []

            self.__system_file_read()
            SystemManager.__instance = self

            global g_SystemManager
            g_SystemManager = self


    def system_file_create(self):
        pass

    def get_user_profiles(self):
        return self.__user_profiles.copy()

    def __system_file_read(self):
        pass

    def logging_history(self):
        pass

    def logging_system_state(self):
        pass

    def logging_error(self):
        pass

    def change_profile(self, index, newProfile):
        pass

    def add_profile(self, userProfile):
        if userProfile:
            self.__user_profiles.append(userProfile)


    def __system_file_write(self):
        pass



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
        return self.password == password

    def set_password(self, new_password):
        self.password = new_password

    def get_name(self):
        return self.__name

    def __str__(self):
        return f"Name: {self.__name}\nEmail: {self.__email}\nDescription: {self.__description}"

    def __eq__(self, other):
        return isinstance(other, UserProfile) and self.get_name() == other.get_name()