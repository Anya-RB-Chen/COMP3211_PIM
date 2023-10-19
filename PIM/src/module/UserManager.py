import os

from PIM.src.model.Contact import Contact
from PIM.src.model.Event import Event
from PIM.src.model.PlainText import PlainText
from PIM.src.model.Task import Task

from PIM.src.module.SystemManager import UserProfile



class UserInformationManager:

    __PIMClassList = [Contact,Event,PlainText, Task]
    # ------------------------------------------------------------------------------------------------------------------------------
    # md 搞不懂python的class字段处理，debug一小时了，还是不行。先这样写吧。 按理来说应该runtime在PIMApp.filesysteminitialization()里面初始化。
    __userFileRootPath =  os.getcwd() + "/file" + "/user"
    __outputFileRootPath =  os.getcwd() + "/file" + "/output"
    # ------------------------------------------------------------------------------------------------------------------------------



    # 1, initialization
    def __init__(self,userProfile:UserProfile) -> None:
        self.userName = userProfile.get_name()

        # (1) file initialization
        # print type for UserInformationManager.__userFileRootPath + self.userName
        # print(UserInformationManager.get_user_file_root_path())
        rootPath = UserInformationManager.get_user_file_root_path()
        self.__userFilePath = rootPath + "/" + self.userName + ".txt"
        if not os.path.exists(self.__userFilePath):
            self.__create()
            self.__PIMList = []
        else:
            self.__PIMList = self.__read()


    # 2, file management 不同文件的读写可以再做封装。
    # (1) user information file
    @classmethod
    def set_user_file_root_path(cls, userFileRootPath):
        # print("set" ,userFileRootPath)
        UserInformationManager.__userFileRootPath = userFileRootPath

    @classmethod
    def get_user_file_root_path(cls):
        # print("get", UserInformationManager.__userFileRootPath)
        return UserInformationManager.__userFileRootPath


    def __create(self):
        pass

    def __read(self):
        pass

    def __write(self):
        pass


    # (2) output file
    @classmethod
    def set_output_file_root_path(cls, outputFileRootPath):
        cls.__outputFileRootPath = outputFileRootPath

    @classmethod
    def get_output_file_root_path(cls):
        return cls.__outputFileRootPath


    def output_user_information(self):
        pass



    # 3, user information management interface
    # get
    def get_PIM_List(self):
        return [pim.copy() for pim in self.__PIMList]

    # operate
    # add the pim. return True if success, False if fail.
    def add_PIM(self, pim):
        if self.contains_name(pim.name):
            return False
        else:
            self.__PIMList.append(pim)
            return True

    def contains_name(self,name):
        pim,index = self.search_name(name)
        return index != -1

    # search the pim name. return the pim if success, None if fail.
    def search_name(self, name):
        index = 0
        for pim in self.__PIMList:
            if pim.name == name:
                return pim,index
            index += 1
        return None,-1

    def modify(self, pim,newPim):
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

