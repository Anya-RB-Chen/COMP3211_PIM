# 用户主页面
from datetime import datetime
from typing import List
from PIM.src.model.Contact import Contact
from PIM.src.model.Event import Event
from PIM.src.model.PIM import PIM
from PIM.src.model.PlainText import PlainText
from PIM.src.model.Task import Task
from PIM.src.tools.Tools import Tools, InputType
from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.module.UserManager import UserInformationManager as User
from PIM.src.module.UserManager import UserIO as IO


class MainPage:

    # level 1: initialization
    def __init__(self) -> None:
        self._userManager = None
        pass

    # level 1: main
    def main(self, userProfile):

        # 0, initialization, welcome message and hint.
        self.ui = InteractiveUI()
        self._userManager = User(userProfile)
        self.ui.print_main_page()
        self.ui.print_user_welcome_message(self._userManager.userName)

        # #alarms/reminders登录检测提醒
        MainPage.check_alarms_or_reminders(User, self._userManager.get_PIM_List())

        moduleNameList = ["Create new PIM", "Manipulate existing PIM", "Generate personal PIM report", "Load PIM file"]
        moduleFunctionList = [self.create_new_PIM, self.manipulate_existing_PIM, self.generate_personal_PIM_report,
                              self.load_PIM_file]
        self.ui.print_choose_hint("", "", moduleNameList)
        choice = self.ui.get_int_input(len(moduleNameList))
        while choice != 0:
            self.ui.print_choose_hint(moduleNameList[choice - 1], "", "")

            moduleFunctionList[choice - 1]()

            self.ui.print_down_line()

            self.ui.print_choose_hint("", "", moduleNameList)
            choice = self.ui.get_int_input(len(moduleNameList))

        # 2, exit
        self.ui.print_leave_main_page()
        # ------------------------------------------------------------------------------------------------------------------------------
        # 文件输出
        self._userManager.write_user_information()

    # ------------------------------------------------------------------------------------------------------------------------------

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

        PIMClassList = User.get_PIMClassList()
        PIMStrList = [C.__name__ for C in PIMClassList]
        self.ui.print_choose_hint("", "", PIMStrList)

        choice = self.ui.get_int_input(len(PIMClassList))
        if choice:
            PIMClass = PIMClassList[choice - 1]

            fields = PIMClass.get_fields()
            checkersMap = PIMClass.get_fields_checkers_map()
            # name = input("Enter the name: ")
            # if not name:
            #     return

            fieldsMap = {}
            for field in fields:
                checker_function = checkersMap[field]

                if field == "start_time" or field == "deadline" or field == " reminder" or field == "alarms":
                    print("Expected format: YYYY-MM-DD HH:MM, e.g., 2023-10-18 14:00")

                content = input(f"Enter the {field} (enter 0 to quit):")

                if content == "0":
                    return

                wrongMessage = checker_function(content)
                while wrongMessage:
                    print(f"Invalid input. {wrongMessage}")
                    content = input("Try again: ")

                    if content == "0":
                        return

                    wrongMessage = checker_function(content)

                fieldsMap[field] = content

            self.ui.print_message("Are you sure to save? (1/0)")
            choice = self.ui.get_int_input(1)
            if choice == 0:
                return

            newPIM = PIMClass.create(fieldsMap["name"], fieldsMap)  # !!!
            self._userManager.add_PIM(newPIM)

    def manipulate_existing_PIM(self):
        self.ui.print_module_in("manipulate existing PIM")

        # 1, search module
        PIMList = self.search_PIM()
        if PIMList == None:
            return

        elif PIMList == []:
            self.ui.print_message("Cannot find the PIM satisfying your criteria.")
            return

        # pre: get valid PIMList
        # 2, print the PIM
        self.ui.print_e_line()
        self.ui.print_message("The PIM in your criteria in as follows: ")
        length = len(PIMList)
        for i in range(length):
            print(f"{i + 1}: ", PIMList[i].__str__())

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
            break

    def generate_personal_PIM_report(self):

        # 1, print the information of PIMs
        self.ui.print_module_in("Generate personal PIM report.")

        PIMList = self._userManager.get_PIM_List()
        self.ui.print_message(f"You have {len(PIMList)}.PIMs in total.")
        if len(PIMList) == 0:  # no PIM no output
            return

        count = 0
        for pim in PIMList:
            count += 1
            print(f"PIM {count}")
            self.ui.print_message(pim.__str__())

        # 2, get the confirm information
        self.ui.print_message("Do you want to output them to a file? (1/0)")
        choice = self.ui.get_int_input(1)
        if choice == 0:
            return

        # 需要增加部分输出
        # self.ui.print_message("You can choose to outpu")
        # 3, output
        self.ui.print_message(
            "Please specify the PIMs you want to print. (e.g., '1 2 3' to print PIM 1, 2, 3)Enter 0 to print all.)")
        choice = self.ui.get_int_input_list(len(PIMList))

        file_name = input(self.ui.print_message("Please enter the file name you want to save as. Enter \" \" "
                                                "to save as your_name.pim."))
        if file_name == " ":
            file_name = self._userManager.userName
        if choice[0] == 0:
            IO(self._userManager).output_user_information(self._userManager.get_PIM_List(), file_name)
        else:
            IO(self._userManager).output_specified_information(self._userManager.get_PIM_List(), choice, file_name)

    def load_PIM_file(self):
        # 1. print hint to load file
        self.ui.print_message("You can have these PIM files. Please choose one to load.")
        # 2. display all files that can be loaded
        IO(self._userManager).display_all_files()
        # 3. enter the file name (error message if not existed)
        file_name = input(self.ui.print_message("Please enter the file's name you want to load(.pim is not required):"))
        # 4. display the content of the pim file
        IO(self._userManager).load_file(file_name)

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

    def search_PIM(self) -> List[PIM]:
        # Step 1: Message

        global results
        self.ui.print_choose_hint("", "Choose a mode of search:", ["Type", "Text", "Time", "Compound condition"])
        choice = self.ui.get_int_input(4)
        if not choice:
            return None

        # Step 2: Functional Module
        if choice == 1:
            self.ui.print_message("Enter the PIM type you're looking for (Task, PlainText, Event, Contact): ")
            inputStr = self.ui.get_correct_input(InputType.PIMTYPE)
            # if not inputStr:
            #     return None
            # if not inputStr:
            pim_type = User.PIM_type_to_class(inputStr)
            PIMList = self._userManager.get_PIM_List()
            results = [pim for pim in PIMList if isinstance(pim, pim_type)]

        elif choice == 2:
            self.ui.print_message("Enter the Text you're looking for: ")
            text = input()
            results = [pim for pim in self._userManager.get_PIM_List() if pim.contain_text(text)]

        elif choice == 3:
            self.ui.print_message("Enter the comparator (<, =, >): ")
            comparator = self.ui.get_correct_input(InputType.COMPARATOR)
            self.ui.print_message("Enter the time (e.g., 2023-10-18 14:00): ")
            time_input = self.ui.get_correct_input(InputType.TIME)
            timestamp = Tools.timeStr_to_timeStamp(time_input)

            results = [pim for pim in self._userManager.get_PIM_List() if
                       pim.time_condition_checker(timestamp, comparator)]

        elif choice == 4:
            self.ui.print_message("Format: type Task &&  text: ! abc || time: < 2023-10-18 14:00")
            self.ui.print_message(
                "Example: To search for Task types that don't contain 'abc' text OR has a time not before '2023-10-18 14:00',\n "
                "input: type: Task && text: ! abc || time: < 2023-10-18 14:00")

            while True:
                condition = self.ui.input_hint("Enter your compound search criteria: ")
                try:
                    # 进行交互，返回查找结果。 如果没找到返回空列表
                    results = MainPage.compound_search(User, self._userManager.get_PIM_List(), condition)
                except Exception as e:
                    print(e)
                    self.ui.print_message("Invalid input. Try again:")
                    continue
                break

        # Step 3: Return Results
        return results if results else []


    @staticmethod
    def compound_search(User, PIMList, condition):
        condition = condition.strip()
        result = ""
        stack = []
        for i in range(len(condition)):
            char = condition[i]
            if char.isspace() or char.isalnum() or char in ["<", ">", "=", "-", ":", "!"]:
                result += char
            # elif char == "(":
            #     stack.append(char)
            # elif char == ")":
            #     result += " "
            #     while (len(stack) != 0) and (stack[-1] != "("):
            #         result += stack.pop()
            #
            #     stack.pop()
            else:
                if len(stack) != 0:
                    if char == stack[-1]:
                        stack[-1] += char
                    else:
                        while len(stack) != 0:
                            if stack[-1] == "||" or stack[-1] == "&&":
                                result += stack.pop()
                            else:
                                break
                        stack.append(char)
                else:
                    stack.append(char)

        result += " "
        while len(stack) != 0:
            #if stack[-1] == "(": return "Invalid Expression"
            if stack[-1] == "||" or stack[-1] == "&&":
                result += stack.pop()
            else:
                break
            if len(stack) != 0 and len(stack) != 1:
                if (result[-1] == "|" and result[-2] == "|") or (result[-1] == "&" and result[-2] == "&"):
                    result += " "

        handle = result.split(" ")
        handle2 = []
        for j in handle:
            if len(j) != 0:
                handle2.append(j)
        compound_lst = [char for char in handle2 if char in ['||', '&&']]
        handle2 = [char for char in handle2 if char not in ['||', '&&']]


        condition_index = []
        condition_lst = []
        for j in range(len(handle2)):
            if handle2[j].lower() in ["type:", "text:", "time:"]:
                condition_index.append(j)
        for i in range(len(condition_index)):
            if condition_index[i] == condition_index[-1]:
                condition_lst.append({handle2[condition_index[i]].lower(): " ".join(handle2[condition_index[i] + 1:])})
            else:
                condition_lst.append({handle2[condition_index[i]].lower(): " ".join(
                    handle2[condition_index[i] + 1:condition_index[i + 1]])})

        result_lst = []
        for request in condition_lst:
            turn = False
            if "type:" in request.keys():
                inputStr = request["type:"]
                if inputStr[0].strip() == "!":
                    turn = True
                    inputStr = request["type:"].strip()[1:].strip()
                pim_type = User.PIM_type_to_class(inputStr)
                results = [pim for pim in PIMList if isinstance(pim, pim_type)]
                if turn:
                    results = [pim for pim in PIMList if pim not in results]
                result_lst.append(results)
            if "text:" in request.keys():
                if request["text:"].strip()[0] == "!":
                    turn = True
                    request["text:"] = request["text:"].strip()[1:].strip()
                results = [pim for pim in PIMList if pim.contain_text(request["text:"])]
                if turn:
                    results = [pim for pim in PIMList if pim not in results]
                result_lst.append(results)
            if "time:" in request.keys():
                input = request["time:"].strip()
                if input[0] == "!":
                    turn = True
                    input = request["time:"][1:]
                comparator = input.strip()[0]
                time_input = input.strip()[1:].strip()
                timestamp = Tools.timeStr_to_timeStamp(time_input)
                results = [pim for pim in PIMList if pim.time_condition_checker(timestamp, comparator)]
                if turn:
                    results = [pim for pim in PIMList if pim not in results]
                result_lst.append(results)

        if len(result_lst) == 0:
            return None

        for condition in compound_lst:
            if condition == '||':
                condition1 = result_lst[0]
                condition2 = result_lst[1]
                del result_lst[0]
                result_lst[0] = [pim for pim in (condition1 or condition2)]
            elif condition == '&&':
                condition1 = result_lst[0]
                condition2 = result_lst[1]
                del result_lst[0]
                result_lst[0] = [pim for pim in (condition1 and condition2)]
            else:
                print("Invalid Expression")

        answer_lst = result_lst[0]
        return answer_lst

