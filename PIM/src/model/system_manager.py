import os
from PIM.src.file_manager.system_file_manager import SystemFileManager
from PIM.src.model.user_profile import UserProfile

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
        self.__systemFileManager.write(self.__user_profiles)

    def get_user_profiles(self):
        return self.__user_profiles.copy()

    def add_profile(self, userProfile):
        if userProfile:
            self.__user_profiles.append(userProfile)





