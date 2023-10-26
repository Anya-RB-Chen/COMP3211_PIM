


# 单例模式 + 全局变量解决访问问题。  （类方法无法整合字段，失去变相对象意义； 不用全局变量传递对象不方便）
from PIM.src.model.Contact import Contact
from PIM.src.model.Event import Event
from PIM.src.model.PIM import PIM
from PIM.src.model.PlainText import PlainText
from PIM.src.model.Task import Task
from PIM.src.module.CMDLineIntepreter import CMDLineIntepreter
from PIM.src.module.Logger import Logger
from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.tools.Tools import InputType, Tools

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

import os


class UserInformationManager:

    __PIMClassList = [Contact,Event,PlainText, Task]
    __userFileRootPath = None
    __outputFileRootPath = None


    # 1, initialization
    def __init__(self,userProfiles:UserProfile) -> None:
        self.userName = userProfiles.get_name()

        # (1) file initialization
        self.__userFilePath = UserInformationManager.__userFileRootPath + self.userName + ".txt"
        if not os.path.exists(self.__userFilePath):
            self.__create()
            self.__PIMList = []
        else:
            self.__PIMList = self.__read()


    # 2, file management 不同文件的读写可以再做封装。
    # (1) user information file
    @classmethod
    def set_user_file_root_path(cls, userFileRootPath):
        cls.__userFileRootPath = userFileRootPath

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

    def output_user_information(self):
        pass



    # 3, user information management interface
    # get
    def get_PIM_List(self):
        return [pim.copy() for pim in self.__PIMList]

    # operate
    # add the pim. return True if success, False if fail.
    def add_PIM(self, pim):
        if self.contains_name(pim.get_name()):
            return False
        else:
            self.__PIMList.append(pim)
            return True

    def contains_name(self,name):
        return self.search_name(name) != None

    # search the pim name. return the pim if success, None if fail.
    def search_name(self, name):
        for pim in self.__PIMList:
            if pim.get_name() == name:
                return pim
        return None

    def modify(self, pim,newPim):
        # search the pim
        index = self.__PIMList.index(pim)
        if index == -1:
            return False

        # modify the pim
        self.__PIMList[index] = newPim
        return True

    def delete(self, pim):
        # search the pim
        index = self.__PIMList.index(pim)
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
        PIMTypeToClassMap = {
            "Contact": Contact,
            "Event": Event,
            "PlainText": PlainText,
            "Task": Task
        }
        if type in PIMTypeToClassMap:
            return PIMTypeToClassMap[type]
        else:
            return None





# 用户主页面

class MainPage:

    # level 1: initialization
    def __init__(self) -> None:
        self.__userManager = None
        pass


    # level 1: main
    def main(self,userProfile):

        # 0, initialization, welcome message and hint.
        self.ui = InteractiveUI()
        self.__userManager = UserInformationManager(userProfile)
        self.ui.print_main_page()
        self.ui.print_user_welcome_message(self.__userManager.userName)
        self.ui.print_message("ps: You can tap or enter 0 to quit the module whenever you want.")

        # 1, main interaction and functional module

        moduleNameList = ["create new PIM", "manipulate existing PIM", "generate personal PIM report"]
        moduleFunctionList = [self.create_new_PIM,self.manipulate_existing_PIM, self.generate_personal_PIM_report]

        self.ui.print_choose_hint("", "", "1-- create 2--search 3--modify 4--delete 5--export")
        choice = self.ui.get_int_input(5)
        while choice != 0:
            self.ui.print_choose_hint(moduleNameList[choice-1],"","")

            moduleFunctionList[choice - 1]()

            self.ui.print_down_line()

            self.ui.print_choose_hint("", "", "1-- create 2--search 3--modify 4--delete 5--export")
            choice = self.ui.get_int_input(5)

        # 2, exit
        self.ui.print_module_out("Main page")


    # ------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def set_output_root_path(cls, outputRootPath):
        cls.__outputFilePath = outputRootPath


    # level 2: specific functional module
    # 统一接口：
    # input : no 进入功能模块。 无需要准备
    # output： 交互、执行功能模块， 直接返回 no return value.

    # 1, create
    # 输出： 添加有效信息 -- add the PIM into system， 打印PIM信息。  中途选择退出： 直接返回
    # 交互过程：
    # （1） 现在仅仅进行基本交互模式：分支模式选择，线性信息输入。
    # 之后可以补充更多模式：比如组快输入（一次性输入多条信息）， 比如不同字段一起输入。 task name dealine ---
    def create_new_PIM(self):
        self.ui.print_module_in("Create new PIM.")

        moduleMessaame = "Which type of the task do you want to create? "
        self.ui.print_message(moduleMessaame)

        PIMClassList = UserInformationManager.get_PIMClassList()
        PIMStrList = [C.__name__ for C in PIMClassList]
        self.ui.print_choose_hint("","",PIMStrList)

        choice = self.ui.get_int_input(len(PIMClassList))
        if choice:
            PIMClass = PIMClassList[choice - 1]

            fields = PIMClass.get_fields()
            checkersMap =  PIMClass.get_fields_checkers_map()
            name = input("Enter the name: ")
            if not name:
                return

            fieldsMap = {}
            for field in fields:
                checker_function = checkersMap[field]

                content = input(f"Enter the {field}: ")
                if not content:
                    return

                wrongMessage = checker_function(content)
                while wrongMessage:
                    print(f"Invalid input. {wrongMessage}")
                    content = input("Try again: ")

                fieldsMap[field] = content

            newPIM = PIMClass.create(name, fieldsMap)
            self.__userManager.add_PIM(newPIM)



    def manipulate_existing_PIM(self):
        self.ui.print_module_in("manipulate existing PIM")

        # 1, search module
        PIMList = self.search_PIM()
        if PIMList == None:
            return

        elif PIMList == []:
            self.ui.print_message("Cannot find the PIM satifying your criteria.")
            return

        # pre: get valid PIMList
        # 2, print the PIM
        self.ui.print_e_line()
        self.ui.print_message("The PIM in your criteria in as follows: ")
        length = len(PIMList)
        for i in range(length):
            print(f"{i+1}: ", PIMList[i].__str__())

        self.ui.print_message("\nYou can modify the or delete some of them.")

        # 3, following operations
        """
        PIMList
        interact with user to get the operation.
        1, print the input prompt (instruction, format, example )
        synatex: example
            # delete 1 2 4 10
            # modify 1 2 3
            # 0 or ""   -> quit directly (return noting)

            operation: delete or modify    +   index of the PIMs.

        2, get user input.
           check the validity of input:
           1) correct instruction name,  if not: give the hint to show the instruction name is wrong
           2) correct index (from 1), if not: give the hint to show the index is out of boundary or in wrong format (not int)
           if the input is invalid, give the reminder and ask user to input again.

        3, get the related part of PIMList.
        involke the related submodule:
        delete(PIMList)   modify(PIMList)
        """

        while True:  # Continue until valid input or exit
            # 1, print the input prompt
            self.ui.print_message(
                "Enter your operation (e.g., 'delete 1 2 4 10' or 'modify 1 2 3'). Enter '0' or '' to quit.")
            user_input = input().strip()

            # Exit conditions
            if user_input in ["", "0"]:
                return

            # Split input into operation and indices
            parts = user_input.split()
            if not parts:
                self.ui.print_message("Invalid input. Please follow the given format.")
                continue

            operation = parts[0].lower()
            indices = parts[1:]

            # 2, check the validity of input
            if operation not in ["delete", "modify"]:
                self.ui.print_message(f"Invalid operation '{operation}'. Valid operations are 'delete' or 'modify'.")
                continue

            try:
                indices = [int(index) for index in indices]
                # Check if indices are in valid range
                if any(index < 1 or index > length for index in indices):
                    raise ValueError("Index out of range")
            except ValueError as e:
                self.ui.print_message(f"Invalid input: {e}. Please enter valid indices.")
                continue

            # 3, get the related part of PIMList
            selected_PIMs = [PIMList[i - 1] for i in indices]

            # Invoke the related submodule
            if operation == "delete":
                self.delete_PIM(selected_PIMs)
            elif operation == "modify":
                self.modify_PIM(selected_PIMs)



    def generate_personal_PIM_report(self):
        pass

# ------------------------------------------------------------------------------------------------------------------------------
    # level 3 细化功能模块以及

    # 2, search
    # requirement discription
    """
    As a user, I want to search for PIMs based on criteria concerning their types and the data stored in their fields.
    whether the PIM belongs to a type.
    whether a piece of text (stored in a note, a description, a name, an address, or a mobile number) contains a string,
    whether a time (stored in a deadline, a starting time, or an alarm) is before (<), after (>), or equal to (=) another given point in time,
    whether a condition combining multiple other conditions via logical connectors and (&&), or (||), and negation (!)
    """

    # interface
    """
    UserManager:
    self.__userManager.get_PIM_List() get all of the PIM of the user.

    PIM:
    contain_text()  # 输入： 文本字符串  # 输出： True or False
    time_condition_checker(time:float, comparator: str)     # 输入： 时间戳，比较符号： 限制 < = > 三种  # 输出： True or False
    """

    # NL description of system (solution)
    """
    input:  no
    output:  [user want to quit] -- None,  [no search result] -- empty list []   [search successfully] -- list[PIM]

    logit:
    1，message
    the search module have 4 way of search: type, text, time, and compound condition.
    The prompt hint will be printed first and allow user the choose one mode. (use the united ui interface)
    2, functional module
    (1)  in every modules, interact with the user to get further input. check the validity of the input
    (2) in the compound search module. print the hint to user to explain format requirement of the input, with one example and explaination.
        then allow the uesr to input one line of the text to represent command:
        the user's input will be like this:  "type Task && (text abc || time < 2023-10-18 14:00)"
    3, Do the search. return the PIM list. if no elements, return empty list [].

    if the input is in wrong format, the system will remind the user with the issue and allow the user to enter again.
    (system will not break because of any user input)
    # interface:
    #   checker_function = get_type_format_checker(inputType): get the format checker function for specific type.
    #   checker_function (value) -> return wrong message if invalid, empty string "" if valid.
    if the user enter "" or "0" the system quit with return value None.
    """

    def search_PIM(self) -> list[PIM]:
        # Step 1: Message

        self.ui.print_choose_hint("", "Choose a mode of search:",["Type", "Text", "Time", "Compound condition"])
        choice = self.ui.get_int_input(4)
        if not choice:
            return None

        # Step 2: Functional Module
        if choice == 1:
            self.ui.print_message("Enter the PIM type you're looking for: ")
            inputStr = self.ui.get_correct_input(InputType.PIMTYPE)
            pim_type = UserInformationManager.PIM_type_to_class(inputStr)
            results = [pim for pim in self.__userManager.get_PIM_List() if isinstance(pim, pim_type)]

        elif choice == 2:
            self.ui.print_message("Enter the Text you're looking for: ")
            text = input()
            results = [pim for pim in self.__userManager.get_PIM_List() if pim.contain_text(text)]

        elif choice == 3:
            self.ui.print_message("Enter the comparator (<, =, >): ")
            comparator = self.ui.get_correct_input(InputType.COMPARATOR)
            self.ui.print_message("Enter the time (e.g., 2023-10-18 14:00): ")
            time_input = self.ui.get_correct_input(InputType.TIME)
            timestamp = Tools.timeStr_to_timeStamp(time_input)

            results = [pim for pim in self.__userManager.get_PIM_List() if
                       pim.time_condition_checker(timestamp, comparator)]

        elif choice == 4:
            print("Format: type Task && (text abc || time < 2023-10-18 14:00)")
            print("Example: To search for a Task type that contains 'abc' text OR has a time before '2023-10-18 14:00',\n "
                  "input: type Task && (text abc || time < 2023-10-18 14:00)")
            while True:
                compound_input = self.ui.input_hint("Enter your compound search criteria: ")
                if compound_input in ["", "0"]:
                    return None
                results = self.compound_search_command_parser(compound_input)
                if results:  # Assuming compound_search_command_parser returns an empty list for invalid input
                    break
                self.ui.print_message("Invalid input. Try again:")

        # Step 3: Return Results
        return results if results else []


    # level 3 compound search parser
    def compound_search_command_parser(self, compound_input: str) -> list:
        while True:
            compound_input = self.ui.input_hint("Enter your compound search criteria: ")
            if compound_input in ["", "0"]:
                return None

            # Splitting the input based on logical connectors
            elements = compound_input.split()

            # List to store results from individual conditions
            results_list = []

            # Handle each element in the compound command
            i = 0
            valid_input = True  # Track if the entire input is valid
            while i < len(elements):
                negate_next = False # handle the negation !

                if elements[i] == "!":
                    negate_next = True
                    i += 1

                elif elements[i] == "type":
                    pim_type_str = elements[i + 1]
                    checker_function =Tools.get_type_format_checker(InputType.PIMTYPE)
                    error_msg = checker_function(pim_type_str)
                    if error_msg:
                        self.ui.print_message(error_msg + ". Try again:")
                        valid_input = False
                        break
                    pim_type = UserInformationManager.PIM_type_to_class(pim_type_str)
                    # add
                    current_results = [pim for pim in self.__userManager.get_PIM_List() if isinstance(pim, pim_type)]
                    if negate_next:
                        current_results = [pim for pim in self.__userManager.get_PIM_List() if
                                           pim not in current_results]
                    results_list.append(current_results)
                    i += 2

                elif elements[i] == "text":
                    text = elements[i + 1]
                    # For "text", we don't have a specific format, so we can directly search.
                    # However, if there are specific format requirements, we can incorporate them.
                    current_results = [pim for pim in self.__userManager.get_PIM_List() if pim.contain_text(text)]
                    if negate_next:
                        current_results = [pim for pim in self.__userManager.get_PIM_List() if
                                           pim not in current_results]
                    results_list.append(current_results)
                    i += 2

                elif elements[i] == "time":
                    comparator = elements[i + 1]
                    checker_function = Tools.get_type_format_checker(InputType.COMPARATOR)
                    error_msg = checker_function(comparator)
                    if error_msg:
                        self.ui.print_message(error_msg + ". Try again:")
                        valid_input = False
                        break

                    time_input = elements[i + 2]
                    checker_function = Tools.get_type_format_checker(InputType.TIME)
                    error_msg = checker_function(time_input)
                    if error_msg:
                        self.ui.print_message(error_msg + ". Try again:")
                        valid_input = False
                        break

                    timestamp = Tools.timeStr_to_timeStamp(time_input)

                    current_results = [pim for pim in self.__userManager.get_PIM_List() if
                                         pim.time_condition_checker(timestamp, comparator)]
                    if negate_next:
                        current_results = [pim for pim in self.__userManager.get_PIM_List() if
                                           pim not in current_results]
                    results_list.append(current_results)
                    i += 3

                else:
                    i += 1

            if not valid_input:
                continue  # Continue asking for input if the current input is invalid

            # Combine results based on logical connectors
            final_results = set(results_list[0])
            for i, element in enumerate(elements[1:], start=1):
                if element == "&&":
                    final_results.intersection_update(set(results_list[i]))
                elif element == "||":
                    final_results.update(set(results_list[i]))
                # Handle negation (!) if needed

            return list(final_results)
    # ------------------------------------------------------------------------------------------------------------------------------
    # 3, modify
    # 对于每一个PIM 提供交互界面让用户指明 更改字段，输入新内容， （有效性查验， 名字需要查看是否重复）
    # 完成以后进行调用 __userManager 接口在用户信息内进行更改。

    def modify_PIM(self,PIMList:list[PIM]):
        self.ui.print_e_line()
        self.ui.print_message(f"You have {len(PIMList)} to manipulate.")
        self.ui.print_message("Let's manipulate the PIM now!")

        count = 0
        for pim in PIMList:
            # (1) print original infromation
            count += 1
            self.ui.print_message(f"Round {count}\n"
                                  f"Original:  {pim.__str__}", )

            # (2) interact to get new information
            fieldsList = pim.get_fields()
            newPim = pim.copy()
            # allow user to enter number to chooce the field to be changed (0 to quit) or use the name to indicate (enter "" to skip enter q to quit and back to main page)
            # 1' indicate fields

            self.ui.print_choose_hint("", "", ["name"] + fieldsList)
            choice = self.ui.get_int_input(len(fieldsList) + 1)
            while choice:
                if choice == 1:
                    field = "name"
                    input_field = input()
                    if input_field in ['0', ""]:
                        break

                    while self.__userManager.contains_name(input_field):
                        self.ui.print_message("The name already exist. please change another name.")
                        input_field = input()
                        if input_field in ['0', ""]:
                            break
                else:
                    field = fieldsList[choice-2]

                    # 2' input new and check validity
                    self.ui.print_message(f"Enter the {field}")
                    input_field = newPim.get_field_input(field)
                    if not input_field: # 如果不进行有效输入 说明用户想退出。
                        break

                # 3' change the field.
                newPim.__setattr__(field,input_field)

                # 4, next round
                self.ui.print_choose_hint("", "", fieldsList)
                choice = self.ui.get_int_input(len(fieldsList))

            # (3) print new inforamtion.
            self.ui.print_message(f"After manipulation. The new information: {newPim}")

            # (4) change in userManager
            self.__userManager.modify(pim,newPim)

    # 4, delete
    def delete_PIM(self,PIMList:list[PIM]):
        # 1, print the information of PIMs
        self.ui.print_e_line()
        self.ui.print_message(f"You have {len(PIMList)} to delete.")
        count = 0
        for pim in PIMList:
            count += 1
            print(f"PIM {count}", end=" ")
            self.ui.print_message(pim.__str__())

        # 2, get the confirm information
        self.ui.print_message("Are you sure to delete them? (1/0)")
        choice = self.ui.get_int_input(1)
        if choice == 0:
            return

        # 3, delete
        for pim in PIMList:
            self.__userManager.delete(pim)

        # 4, print message
        self.ui.print_message("Delete successfully!")

    # 5, output
    def output_PIM(self, PIMList:list[PIM]):
        # 1, print the information of PIMs
        self.ui.print_e_line()
        self.ui.print_message(f"You have {len(PIMList)}.")
        count = 0
        for pim in PIMList:
            count += 1
            print(f"PIM {count}", end=" ")
            self.ui.print_message(pim.__str__())

        # 2, get the confirm information
        self.ui.print_message("Do you want to output them to a file? (1/0)")
        choice = self.ui.get_int_input(1)
        if choice == 0:
            return

        # 3, output
        self.__userManager.ouput_user_information()


import os
import traceback

# 10.14 1h 自顶向下 XP实现。
# User story. no -- 用流程图
# 直接面向过程，自顶向下面向对象搭建。

# 对于面向过程的设计，依然用对象的方式实现，毕竟这样可以实现多线程，多用户同时用一个程序登录。 虽然者没什么用
# 如果设计模式不好，等着改掉。现在没时间研究这些细节。
class PIMApp:


    # level 0
    __logFilePath = None
    __systemFilePath = None

    def __init__(self): # 先不用单例模式。直接把系统文件作为字段来使用。
        # file system initialization
        self.file_system_initialization()

       # 系统模块初始化
        self.systemManager = SystemManager(PIMApp.__systemFilePath)
        self.logger = Logger(PIMApp.__logFilePath)

       # ------------------------------------------------------------------------------------------------------------------------------
       # 测试
       #  self.systemManager.add_profile(UserProfile("Mike", "123456", "21100038d@connect.polyu.hk", "hhh"))
       # ------------------------------------------------------------------------------------------------------------------------------

        # userProfiles = self.systemManager.get_user_profiles()
        # self.loginSystem =
        self.mainPage = MainPage()
        self.cmdIntepreter = CMDLineIntepreter()


    # level 0 : 自顶向下开发， 设计 - 开发 - 建模 三部分同步，形成高效信息循环。按照实际场景做建模，根据模型做设计，根据设计做开发。
    # 即时性的反馈 +  系统性的开发方法。

    def main(self):
        ui = InteractiveUI()
        # 1, welcome message and hint.
        ui.print_welcome_message()

        # 2, page 1: log in system | register | command mode
        choice = "1 --log in  2 --register 3--command mode. 0-- quit"
        ui.print_choose_hint("","",choice)

        choice = ui.get_int_input(3) #

        # 2,
        try:
            if choice == 1: # 登录 -- 进入系统
                userProfile = self.login()
                if userProfile:
                    self.mainPage.main(userProfile)


            elif choice == 2: #注册 -- 进入系统
                userProfile = self.register()
                ui.print_choose_hint("","Do you want to log in directly?", "1-- yes")
                choice1 = ui.get_int_input(1)
                if choice1:
                    self.mainPage.main(userProfile)

            else: # cmd模式。 需要改交互方式。 这只作为一个 prototype
                self.cmdLineMode()

        except Exception:
            print("Error happends in welcome page.")
            traceback.print_exc()
            return -1


        # 3，
        ui.print_leave_message()
        self.system_clear_up()



# ------------------------------------------------------------------------------------------------------------------------------
    # level 1

    # file system initialzation
    def file_system_initialization(self):
        # root folder initialization
        root_path = os.getcwd() + "/file"
        if not os.path.exists(root_path):
            os.mkdir(root_path)

        # system file initialization
        PIMApp.__systemFilePath = root_path + "/system.txt"

        # user directory initialization
        userFileRootPath = root_path + "/user"
        if not os.path.exists(userFileRootPath):
            os.mkdir(userFileRootPath)
        UserInformationManager.set_user_file_root_path(userFileRootPath)

        # output directory initialization
        outputRootPath = root_path + "/output"
        if not os.path.exists(outputRootPath):
            os.mkdir(outputRootPath)
        MainPage.set_output_root_path(outputRootPath)

        # log file initialization
        PIMApp.__logFilePath = root_path + "/log.txt"

    # 登录系统：
    # input: no  采取最简单的设计，直接启动系统。 可以改成名字等
    # output： user profile.  None is not successfull

    #下层接口： g_SystemManager.get_user_profile()  -- 登录属于业务逻辑，与底层分开。
    # 1, ask the user to input name. (if enter 0, return None) 2, search name in the system. all of the user profiles can be obtained by self.get_user_profiles() method (a list of UserProfile objects), and the UserProfile object have "==" operator.  3, if the name not in the system,  return None. otherwise, ask for enterring password (in UserProfile: check_password() -> bool ). There are 3 chances at all. if the input is correct, return userProfile. otherwise, return None.
    def login(self):
        name = input("Please enter your name: ")
        if name == "0":
            return None
        user_profiles = self.systemManager.get_user_profiles()
        if user_profiles:
            for user_profile in user_profiles:
                if user_profile.get_name() == name:
                    for i in range(3):
                        password = input("Please enter your password: ")
                        if user_profile.check_password(password):
                            return user_profile
                    print("wrong password. Sorry.")
                    return None
            print("Sorry, cannot find you in system.")
        return None

    # 1,
    # input: no
    # output: quit -> return None,  |  successful -> return UserProfile, add valid user profile to system.

    # (1) ask the user to enter the user name. use Tools.checkNameAvailable(name) to check whether the format of name is valid (define by yourself what is invalid format for name and implement this method with annotation to explain your standard)
    # (2) search the user name in user profiles list (self.systemManager.get_user_profiles()) if the name already in system, give the hint to user and allow user to reenter a name.
    # (3) ask the user to enter the password. check whether the password is strong enough by Tools.checkPasswordStrength(password) (the standard also defined by you, and implement the method with annotation)
    #     if the password is not strong, give the user hint to ask the user whether he want to keep the password or use new one. If he want to use new one, allow him to set the password again.
    # (4) ask the user to add additional information: Email, and description, but this is optional.
    # (5) create the UserProfile object for user and use g_SystemManager.add_profile() to add it into system
    # (6) print the message "successfully register as new patron to the PIM system. Welcome !
    #
    # ps: In every round, there should have a hint (enter 0 to quit), if the user enter 0, return None

    def register(self):
        while True:
            # name
            name = input("Please enter your name (enter 0 to quit): ")
            if name == "0":
                return None
            if not Tools.checkNameAvailable(name):
                print("Invalid name format. Please try again.")
                continue
            user_profiles = self.systemManager.get_user_profiles()
            if user_profiles and UserProfile(name,"") in user_profiles:
                print("This name already exists. Please try again.")
                continue

            # password
            while True:
                password = input("Please enter your password (enter 0 to quit): ")
                if password == "0":
                    return None
                if not Tools.checkPasswordStrength(password):
                    print("Weak password. Do you want to keep it? (y/n)")
                    choice = input()
                    if choice.lower() == "n":
                        continue
                break

            # additional information
            email = input("Please enter your email (optional, enter 0 to skip): ")
            while email != "0" and not Tools.is_valid_email(email):
                email = input("Invalid Email. Input again. (enter 0 to skip)")
            if email == "0":
                email = ""

            description = input("Please enter a description (optional, enter 0 to skip): ")
            if description == "0":
                description = ""

            # add to system.
            user_profile = UserProfile(name, password, email, description)
            self.systemManager.add_profile(user_profile)
            print("Successfully registered as a new patron to the PIM system. Welcome!")

            return user_profile

# ------------------------------------------------------------------------------------------------------------------------------
    # 拓展功能 -- 留存

    def cmdLineMode(self):
        pass
 # ------------------------------------------------------------------------------------------------------------------------------

    # clear the resource of system
    def system_clear_up(self):
        pass
