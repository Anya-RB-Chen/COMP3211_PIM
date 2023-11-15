import os
from datetime import datetime
import time
import stat

from colorama import Fore

from PIM.src.model.Contact import Contact
from PIM.src.model.Event import Event
from PIM.src.model.PlainText import PlainText
from PIM.src.model.Task import Task

from PIM.src.module.SystemManager import UserProfile
from PIM.src.tools.Tools import Tools


# 思路：将修改/添加PIM与load/save PIM分为两个class，IO只管单纯的文件读写


class UserInformationManager:
    __PIMClassList = [Contact, Event, PlainText, Task]
    # ------------------------------------------------------------------------------------------------------------------------------
    # md 搞不懂python的class字段处理，debug一小时了，还是不行。先这样写吧。 按理来说应该runtime在PIMApp.filesysteminitialization()里面初始化。
    __userFileRootPath = os.getcwd() + "/file" + "/user"

    # ------------------------------------------------------------------------------------------------------------------------------

    # 1, initialization
    def __init__(self, userProfile: UserProfile) -> None:
        self.logInTimeStamp = time.time()
        self.userName = userProfile.get_name()

        # (1) file initialization
        # print type for UserInformationManager.__userFileRootPath + self.userName
        # print(UserInformationManager.get_user_file_root_path())
        rootPath = UserInformationManager.get_user_file_root_path()
        self.__userFilePath = rootPath + "/." + self.userName + ".txt"
        if not os.path.exists(self.__userFilePath):
            self.__create()
            self.__PIMList = []
            self.__history = []
        else:
            print("read from txt file")
            self.__PIMList, self.__history = self.__read()

    # 2, file management 不同文件的读写可以再做封装。
    # (1) user information file management
    # file path: self.__userFilePath  (./file/user)
    # file name: f{self.username}.txt (name.txt)

    # non functional： 1， 安全： 访问 0644（其他人不能删除） 2， 内容加密
    # functional： 1， 需要改成 append 模式    2， 需要增加安全性，（系统崩溃恢复原始文件。
    @classmethod
    def set_user_file_root_path(cls, userFileRootPath):
        # print("set" ,userFileRootPath)
        UserInformationManager.__userFileRootPath = userFileRootPath

    @classmethod
    def get_user_file_root_path(cls):
        # print("get", UserInformationManager.__userFileRootPath)
        return UserInformationManager.__userFileRootPath

    # mode: 0644. the file cannot be deleted by others.
    # the empty file should be able to be read correctly without errors.
    def __create(self):
        if not os.path.exists(self.__userFilePath):
            # 先不进行框架的print，因为在结束的write方法后，会把内容连同字段一起写入文件

            with open(self.__userFilePath, "w") as f:
                pass
            os.chmod(self.__userFilePath, 0o644)

    # format
    """
    History:
    time1 log in  |  time2 log out 
    ...

    Personal information records:
    PIM 1
    content of pim

    PIM 2
    ....

    """

    # example
    """
    history:
    2023-12-01 19:00 log in  |  2023-12-01 19:30 log out
    2023-12-01 20:00 log in  |  2023-12-01 20:30 log out


    personal information records: 

    PIM 1
    Name: John Doe
    Type: Contact
    Mobile number: 123-456-7890
    Address: 123 Elm St.

    PIM 2
    Name: Jane Smith
    Type: Contact
    Mobile number: 234-567-8901
    Address: 456 Oak St.

    PIM 3
    Name: Buy groceries
    Type: Task
    Description: Buy milk, bread, and eggs
    Deadline: 2023-10-25 09:00
    Reminder: 
    """

    # interface:
    # 1, PIM.__str__ get the string output format of PIM type.   2, Tools.timeStamp_to_timeStr(timeStamp)
    # contents: 1, self.__PIMList pim list  2, previous log in/out time self.__history  + current log in time self.logInTimeStamp log out time: now.
    # output: PIMList list[PIM]  history list[[log_in_time_str, log_out_time_str]]

    def __read(self):
        with open(self.__userFilePath, "r") as f:
            lines = f.readlines()
            history = []
            PIMList = []
            reading_history = False
            reading_pim_records = False
            index = 0

            length = len(lines)
            while index < length:
                line = lines[index]

                if line == "\n":
                    index += 1
                    continue

                if line.startswith("History:"):
                    reading_history = True
                    reading_pim_records = False

                elif line.startswith("Personal Information Records:"):
                    reading_history = False
                    reading_pim_records = True

                elif reading_pim_records:
                    if line.startswith("PIM"):
                        # assumption type 在第二行
                        pim_type = lines[index + 2].strip().split(":")[1].strip()
                    else:
                        pim, lineNumbers = self.create_pim_object_from_lines(lines, index, pim_type)

                        PIMList.append(pim)

                        index -= 1
                        index += lineNumbers

                index += 1

            return PIMList, history

    def write(self):
        with open(self.__userFilePath, "w") as f:
            f.write("History:\n\n")
            for log_in_time, log_out_time in self.__history:
                f.write(f"{log_in_time} log in  |  {log_out_time} log out\n")
            if self.logInTimeStamp is not None:
                log_in_time = Tools.timeStamp_to_timeStr(self.logInTimeStamp)
                log_out_time = Tools.timeStamp_to_timeStr(time.time())
                f.write(f"{log_in_time} log in  |  {log_out_time} log out\n")

            f.write("\n\n")

            f.write("Personal Information Records:\n\n")
            index_number = 1
            for pim in self.__PIMList:
                f.write(f"\nPIM {index_number}: \n")
                index_number += 1
                f.write(str(pim))
                f.write("\n")

    @staticmethod
    def create_pim_object_from_lines(lines, line_index, pim_type) -> (list, int):
        pim_type = pim_type.lower()

        pim_classes = {
            "contact": Contact,
            "task": Task,
            "event": Event,
            "plaintext": PlainText
        }

        pim_class = pim_classes.get(pim_type)
        if pim_class:
            return pim_class.create_object_from_lines(lines, line_index), len(pim_class.get_fields()) + 1

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


class UserIO:
    __outputFileRootPath = os.getcwd() + "/file" + "/output"

    def __init__(self, UserInformationManager):
        self.user = UserInformationManager
        self.userName = self.user.userName
        self.PIMList = self.user.get_PIM_List()

    def set_output_file_root_path(self, outputFileRootPath):
        self.__outputFileRootPath = outputFileRootPath

    def get_output_file_root_path(self):
        return self.__outputFileRootPath

    def output_user_information(self, PIMList, file_name):
        outputFilePath = self.__outputFileRootPath + f"/{self.userName}"
        isExist = os.path.exists(outputFilePath)
        if not isExist:
            os.makedirs(outputFilePath)
        outputFilePath += f"/{file_name}" + ".pim"

        with open(outputFilePath, "w", encoding="utf-8") as f:
            message = """
             ☆──────────────✬❖✬───────────☆
             │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
             │       😄   PERSONAL  😃     │
             │       😆 INFORMATION 😁     │
             │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
             ☆──────────────✬❖✬───────────☆

            """
            f.write(message)
            f.write("\n\n")

            f.write(f"Hi {self.userName}, You have {len(PIMList)} personal information records.")
            f.write("\n\n")

            index_number = 1
            for pim in self.PIMList:
                f.write(f"\nPIM {index_number}: \n")
                index_number += 1
                f.write(str(pim))
                f.write("\n")

    def output_specified_information(self, PIMList, choice, file_name):
        outputFilePath = self.__outputFileRootPath + f"/{self.userName}"
        isExist = os.path.exists(outputFilePath)
        if not isExist:
            os.makedirs(outputFilePath)
        outputFilePath += f"/{file_name}" + ".pim"
        # count = 1
        # while os.path.exists(outputFilePath): # 改为append
        #     outputFilePath = self.__outputFileRootPath + "/" + self.userName + str(count) + ".pim"
        #     count += 1

        with open(outputFilePath, "w", encoding="utf-8") as f:
            message = """
                       ──────────────✬❖✬───────────
                     │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
                     │       😄   PERSONAL  😃     │
                     │       😆 INFORMATION 😁     │
                     │       ❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈❈     │
                       ──────────────✬❖✬───────────

                    """
            f.write(message)
            f.write("\n\n")
            f.write(f"Hi {self.userName}! Here are {len(choice)} personal information records that you selected.")
            f.write("\n\n")

            j = 0
            idx = 1
            while j < len(choice) and idx <= len(PIMList):
                if idx == choice[j]:
                    f.write(f"\nPIM {idx}: \n")
                    f.write(str(self.PIMList[idx - 1]))
                    j += 1
                    idx += 1
                    f.write("\n")
                else:
                    idx += 1

    def display_all_files(self):
        outputFilePath = self.__outputFileRootPath + f"/{self.userName}"
        isExist = os.path.exists(outputFilePath)
        if isExist:
            for file in os.listdir(outputFilePath):
                print(file, "  ", end='')
            print()

    def load_file(self, file_name):
        outputFilePath = self.__outputFileRootPath + f"/{self.userName}/{file_name}.pim"
        try:
            with open(outputFilePath, encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("Please enter the right file name.")