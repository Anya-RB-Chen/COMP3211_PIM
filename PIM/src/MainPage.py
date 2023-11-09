

# 用户主页面
from typing import List

from PIM.src.model.Contact import Contact
from PIM.src.model.Event import Event
from PIM.src.model.PIM import PIM
from PIM.src.model.PlainText import PlainText
from PIM.src.model.Task import Task
from PIM.src.tools.Tools import Tools, InputType
from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.module.UserManager import UserInformationManager as User


class MainPage:

    # level 1: initialization
    def __init__(self) -> None:
        self.__userManager = None
        pass


    # level 1: main
    def main(self,userProfile):

        # 0, initialization, welcome message and hint.
        self.ui = InteractiveUI()
        self.__userManager = User(userProfile)
        self.ui.print_main_page()
        self.ui.print_user_welcome_message(self.__userManager.userName)
        self.ui.print_message("ps: You can tap or enter 0 to quit the module whenever you want.")

        # # # 1, main interaction and functional module
            # ------------------------------------------------------------------------------------------------------------------------------
        if len(self.__userManager.get_PIM_List()) == 0:
            # 测试： 系统内设置PIM信息
            print("测试模式： 系统内设置PIM信息\n")
            # Contact PIMs
            contact1 = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
            contact2 = Contact.create("Jane Smith",
                                      {"mobile_number": "234-567-8901", "address": "456 Oak St."})

            # Task PIMs 有问题
            task1 = Task.create("Buy groceries", {"description": "Buy milk, bread, and eggs", "deadline": "2023-10-25 09:00"})
            task2 = Task.create("Attend meeting",
                                {"description": "Team sync-up", "deadline": "2023-10-21 09:00", "reminder": "2023-10-20 09:00"})

            # Event PIMs
            event1 = Event.create("Birthday party",
                                  {"description": "John's 30th birthday", "start_time": "2023-11-15 19:00",
                                   "alarms": ["2023-11-15 18:30"]})
            event2 = Event.create("Concert", {"description": "Live music by The Beatles", "start_time": "2023-12-01 20:00",
                                              "alarms": ["2023-12-01 19:00", "2023-12-01 19:30"]})

            # PlainText PIMs 有问题
            text1 = PlainText.create("Shopping List", {"text": "Milk, Bread, Eggs, Butter"})
            text2 = PlainText.create("Work Notes", {"text": "Discuss project timeline in the next meeting."})
            text3 = PlainText.create("Poem", {"text": "Roses are red, Violets are blue."})
            text4 = PlainText.create("Quotes", {"text": "Be yourself; everyone else is already taken. - Oscar Wilde"})

            PIMList = [contact1, contact2, task1, task2, event1, event2, text1, text2, text3, text4]
            for pim in PIMList:
                self.__userManager.add_PIM(pim)
                self.ui.print_message(f"Added PIM: {pim}")
            print("\n\n\n")

            # You now have 10 PIM items: 2 Contacts, 2 Tasks, 2 Events, and 4 PlainTexts.

            # # ------------------------------------------------------------------------------------------------------------------------------


        moduleNameList = ["Create new PIM", "Manipulate existing PIM", "Generate personal PIM report","Load PIM file"]
        moduleFunctionList = [self.create_new_PIM,self.manipulate_existing_PIM, self.generate_personal_PIM_report,self.load_PIM_file]

        self.ui.print_choose_hint("", "", moduleNameList)
        choice = self.ui.get_int_input(len(moduleNameList))
        while choice != 0:
            self.ui.print_choose_hint(moduleNameList[choice-1],"","")

            moduleFunctionList[choice - 1]()

            self.ui.print_down_line()

            self.ui.print_choose_hint("", "", moduleNameList)
            choice = self.ui.get_int_input(len(moduleNameList))

        # 2, exit
        self.ui.print_leave_main_page()
        # ------------------------------------------------------------------------------------------------------------------------------
        # 文件输出
        self.__userManager.write()




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
        self.ui.print_choose_hint("","",PIMStrList)

        choice = self.ui.get_int_input(len(PIMClassList))
        if choice:
            PIMClass = PIMClassList[choice - 1]

            fields = PIMClass.get_fields()
            checkersMap =  PIMClass.get_fields_checkers_map()
            # name = input("Enter the name: ")
            # if not name:
            #     return

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

                    wrongMessage = checker_function(content)

                fieldsMap[field] = content

            newPIM = PIMClass.create(fieldsMap["name"], fieldsMap) # !!!
            self.__userManager.add_PIM(newPIM)



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
            break



    def generate_personal_PIM_report(self):

        # 1, print the information of PIMs
        self.ui.print_module_in("Generate personal PIM report.")

        PIMList = self.__userManager.get_PIM_List()
        self.ui.print_message(f"You have {len(PIMList)}.PIMs in total.")
        if len(PIMList) == 0: # no PIM no output
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
        self.ui.print_message("Please specify the PIMs you want to print. Enter 0 to print all.")
        choice = self.ui.get_int_input_list(len(PIMList))
        file_name = input(self.ui.print_message("Please enter the file name you want to save as. Enter \" \" "
                                                "to save as your_name.pim."))
        if file_name == " ":
            file_name = self.__userManager.userName
        # 3, output
        if choice[0] == 0:
            self.__userManager.output_user_information(self.__userManager.get_PIM_List(),file_name)
        else:
            self.__userManager.output_specified_information(self.__userManager.get_PIM_List(),choice,file_name)


    def load_PIM_file(self):
        # 1. print hint to load file
        self.ui.print_message("You can have these PIM files. Please choose one to load.")
        # 2. display all files that can be loaded
        self.__userManager.display_all_files()
        # 3. enter the file name (error message if not existed)

        file_name = input(self.ui.print_message("Please enter the file's name you want to load(.pim is not required):"))

        # 4. display the content of the pim file
        self.__userManager.load_file(file_name)



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

        self.ui.print_choose_hint("", "Choose a mode of search:",["Type", "Text", "Time", "Compound condition"])
        choice = self.ui.get_int_input(4)
        if not choice:
            return None

        # Step 2: Functional Module
        if choice == 1:
            self.ui.print_message("Enter the PIM type you're looking for: ")
            inputStr = self.ui.get_correct_input(InputType.PIMTYPE)
            pim_type = User.PIM_type_to_class(inputStr)
            PIMList = self.__userManager.get_PIM_List()
            results = [pim for pim in PIMList if isinstance(pim, pim_type)]

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
            print("Example: To search for a Task type that contains 'abc' text OR has a time not before '2023-10-18 14:00',\n "
                  "input: type Task && text abc || ! time < 2023-10-18 14:00")
            while True:
                # compound_input = self.ui.input_hint("Enter your compound search criteria: ")
                # if compound_input in ["", "0"]:
                #     return None
                try:
                    # 进行交互，返回查找结果。 如果没找到返回空列表
                    results = self.compound_search_command_parser()
                except Exception as e:
                    self.ui.print_message("Invalid input. Try again:")
                    continue
                break

        # Step 3: Return Results
        return results if results else []


    # level 3 compound search parser
    def compound_search_command_parser(self) -> list:
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
                elements[i] = elements[i].lower()

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
                    pim_type = User.PIM_type_to_class(pim_type_str)
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

                    time_input = elements[i + 2] + " " + elements[i + 3]
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
                    i += 4

                else:
                    i += 1

            if not valid_input:
                continue  # Continue asking for input if the current input is invalid

            # Combine results based on logical connectors
            final_results = set(results_list[0])
            i = 1
            for element in elements[1:]:
                if element == "&&":
                    final_results.intersection_update(set(results_list[i]))
                    i += 1
                elif element == "||":
                    final_results.update(set(results_list[i]))
                    i += 1
                # Handle negation (!) if needed

            return list(final_results)
    # ------------------------------------------------------------------------------------------------------------------------------
    # 3, modify
    # 对于每一个PIM 提供交互界面让用户指明 更改字段，输入新内容， （有效性查验， 名字需要查看是否重复）
    # 完成以后进行调用 __userManager 接口在用户信息内进行更改。

    def modify_PIM(self, PIMList: List[PIM]):
        self.ui.print_e_line()
        self.ui.print_message(f"You have {len(PIMList)} to manipulate.")
        self.ui.print_message("Let's manipulate the PIM now!")

        count = 0
        for pim in PIMList:
            # (1) print original infromation
            count += 1
            self.ui.print_message(f"Round {count}\n"
                                  f"Original: ------->\n{pim}", )

            # (2) interact to get new information
            fieldsList = pim.get_fields()
            newPim = pim.copy()
            # allow user to enter number to chooce the field to be changed (0 to quit) or use the name to indicate (enter "" to skip enter q to quit and back to main page)
            # 1' indicate fields

            self.ui.print_choose_hint("", "", fieldsList)
            choice = self.ui.get_int_input(len(fieldsList))
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
                    field = fieldsList[choice-1]

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
            self.ui.print_message(f"After manipulation. The new information: ----->\n {newPim}")

            # (4) change in userManager
            self.__userManager.modify(pim,newPim)

    # 4, delete
    def delete_PIM(self, PIMList: List[PIM]):
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

    # # 5, output
    # def output_PIM(self, PIMList:list[PIM]):
    #     # 1, print the information of PIMs
    #     self.ui.print_e_line()
    #     self.ui.print_message(f"You have {len(PIMList)}.")
    #     count = 0
    #     for pim in PIMList:
    #         count += 1
    #         print(f"PIM {count}", end=" ")
    #         self.ui.print_message(pim.__str__())
    #
    #     # 2, get the confirm information
    #     self.ui.print_message("Do you want to output them to a file? (1/0)")
    #     choice = self.ui.get_int_input(1)
    #     if choice == 0:
    #         return
    #
    #     # 3, output
    #     self.__userManager.ouput_user_information()

