import os
import time

from PIM.src.model.contact import Contact
from PIM.src.model.event import Event
from PIM.src.model.plain_text import PlainText
from PIM.src.model.task import Task

from PIM.src.model.system_manager import UserProfile
from PIM.src.tools.Tools import Tools
from PIM.src.file_manager.user_file_manager import UserFileManager
from  PIM.src.file_manager.output_file_manager import OutputFileManager as OutputFileManager


# 思路：将修改/添加PIM与load/save PIM分为两个class，IO只管单纯的文件读写


class UserInformationManager:
    __PIMClassList = [Contact, Event, PlainText, Task]
    # ------------------------------------------------------------------------------------------------------------------------------
    # md 搞不懂python的class字段处理，debug一小时了，还是不行。先这样写吧。 按理来说应该runtime在PIMApp.filesysteminitialization()里面初始化。
    __userFileRootPath = os.getcwd() + "/PIM/src/file" + "/user"
    # ------------------------------------------------------------------------------------------------------------------------------

    # 1, initialization
    def __init__(self, userProfile: UserProfile) -> None:
        self.logInTimeStamp = time.time()
        self.userName = userProfile.get_name()

        # (1) file initialization
        # print type for UserInformationManager.__userFileRootPath + self.userName
        # print(UserInformationManager.get_user_file_root_path())

        rootPath = UserInformationManager.get_user_file_root_path()
        userFilePath = rootPath + "/." + self.userName + ".txt"
        self.__userFileManager = UserFileManager(userFilePath)

        self.__PIMList, self.__history = self.__read_user_information()


    # 2, file management 不同文件的读写可以再做封装。
    # (1) user information file management
    # file path: self.__userFilePath  (./file/user)
    # file name: f{self.username}.txt (name.txt)
    @classmethod
    def set_user_file_root_path(cls, userFileRootPath):
        # print("set" ,userFileRootPath)
        UserInformationManager.__userFileRootPath = userFileRootPath

    @classmethod
    def get_user_file_root_path(cls):
        # print("get", UserInformationManager.__userFileRootPath)
        return UserInformationManager.__userFileRootPath


    # interface:
    # 1, PIM.__str__ get the string output format of PIM type.   2, Tools.timeStamp_to_timeStr(timeStamp)
    # contents: 1, self.__PIMList pim list  2, previous log in/out time self.__history  + current log in time self.logInTimeStamp log out time: now.
    # output: PIMList list[PIM]  history list[[log_in_time_str, log_out_time_str]]

    def __read_user_information(self):
        return self.__userFileManager.read()

    def write_user_information(self):
        self.__userFileManager.write()

    # ------------------------------------------------------------------------------------------------------------------------------
    # 3, user information management interface
    # get
    def get_PIM_List(self):
        return self.__PIMList

    # operate
    # add the pim. return True if success, False if fail.
    def add_PIM(self, pim):
        if self.contains_name(pim.name):
            return False
        else:
            self.__PIMList.append(pim)
            return True

    def contains_name(self, name):
        pim, index = self.search_name(name)
        return index != -1

    # search the pim name. return the pim if success, None if fail.
    def search_name(self, name):
        index = 0
        for pim in self.__PIMList:
            if pim.name == name:
                return pim, index
            index += 1
        return None, -1

    def modify(self, pim, newPim):
        # search the pim
        pim, index = self.search_name(pim.name)
        if index == -1:
            return False
        # modify the pim
        self.__PIMList[index] = newPim
        return True

    def delete(self, pim):
        # search the pim
        pim, index = self.search_name(pim.name)
        if index == -1:
            return False

        # delete the pim
        self.__PIMList.pop(index)
        return True

    # 4, pim information
    @classmethod
    def get_PIMClassList(cls):
        return UserInformationManager.__PIMClassList.copy()

    @classmethod
    def PIM_type_to_class(cls, type):
        type = type.lower()

        PIMTypeToClassMap = {
            "contact": Contact,
            "event": Event,
            "plaintext": PlainText,
            "task": Task
        }
        if type in PIMTypeToClassMap:
            return PIMTypeToClassMap[type]
        else:
            return None



