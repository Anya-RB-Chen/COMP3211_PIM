import os
import time

from PIM.src.model.contact import Contact
from PIM.src.model.event import Event
from PIM.src.model.plain_text import PlainText
from PIM.src.model.task import Task

from PIM.src.model.system_manager import UserProfile
from PIM.src.tools.Tools import Tools
from PIM.src.file_manager.user_file_manager import UserFileManager
from PIM.src.file_manager.output_file_manager import OutputFileManager as OutputFileManager


class UserInformationManager:
    """
    This is the class of user information manager. It can reads user's PIM list stored in user file and write the modified
    or new PIM list back to the user file. The user file serves as the storage database of the user's personal information.
    """
    __PIMClassList = [Contact, Event, PlainText, Task]
    __userFileRootPath = os.getcwd() + "/file" + "/user"
    # ------------------------------------------------------------------------------------------------------------------------------
    # 1, initialization
    def __init__(self, userProfile: UserProfile) -> None:
        self.logInTimeStamp = time.time()
        self.userName = userProfile.get_name()

        # (1) file initialization
        rootPath = UserInformationManager.get_user_file_root_path()
        userFilePath = rootPath + "/." + self.userName + ".txt"
        self.__userFileManager = UserFileManager(userFilePath)
        self.__PIMList, self.__history = self.__read_user_information()


    """
     2. file management
     (1) user information file management
     file path: self.__userFilePath  (./file/user)
     file name: f{self.username}.txt (name.txt)
    """
    @classmethod
    def set_user_file_root_path(cls, userFileRootPath):
        UserInformationManager.__userFileRootPath = userFileRootPath

    @classmethod
    def get_user_file_root_path(cls):
        return UserInformationManager.__userFileRootPath

    """
    interface:
        1, PIM.__str__ get the string output format of PIM type.   
        2, Tools.timeStamp_to_timeStr(timeStamp)
    contents: 
        1, self.__PIMList pim list  
        2, previous log in/out time self.__history  + current log in time self.logInTimeStamp log out time: now.
    outputs: 
        PIMList list[PIM]  history list[[log_in_time_str, log_out_time_str]]
    """
    def __read_user_information(self):
        return self.__userFileManager.read()

    def write_user_information(self):
        self.__userFileManager.write()

    # ------------------------------------------------------------------------------------------------------------------------------
    # 3, user information management interface
    # get
    def get_PIM_List(self):
        return self.__PIMList

    def add_PIM(self, pim):
        """
        add the pim.
        :param pim: new PIM
        :return: True if success, False if fail.
        """
        if self.contains_name(pim.name):
            return False
        else:
            self.__PIMList.append(pim)
            return True

    def contains_name(self, name):
        """
        :param name: the search target
        :return:
        """
        pim, index = self.search_name(name)
        return index != -1

    def search_name(self, name):
        """
        search the pim name. return the pim if success, None if fail.
        :param name: the search target
        :return:
        """
        index = 0
        for pim in self.__PIMList:
            if pim.name == name:
                return pim, index
            index += 1
        return None, -1

    def modify(self, pim, newPim):
        """
        This function is to modify a specific PIM.
        :param pim: the original PIM
        :param newPim: the modified PIM
        :return: boolean
        """
        # search the pim
        pim, index = self.search_name(pim.name)
        if index == -1:
            return False
        # modify the pim
        self.__PIMList[index] = newPim
        return True

    def delete(self, pim):
        """
        This function is to delete a specific PIM
        :param pim: the target the user want to delete
        :return:
        """
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
        """
        This function is to convert PIM type to corresponding PIM class.
        :param type: The PIM type the user inputs.
        :return:
        """
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



