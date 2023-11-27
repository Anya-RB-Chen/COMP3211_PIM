from datetime import datetime
from typing import List

from  PIM.src.model import *

from PIM.src.tools.Tools import Tools, InputType
from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.model.user_manager import UserInformationManager as User
from PIM.src.file_manager.output_file_manager import OutputFileManager as IO


class MainPage:
    """
    Main page for each user. Should be displayed after logging into the system.
    """
    # level 0: initialization
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

        # #alarms/reminders
        MainPage.check_alarms_or_reminders(User, self._userManager.get_PIM_List())

        moduleNameList = ["Create new PIM", "Manipulate existing PIM", "Generate personal PIM report", "Load PIM file"]
        moduleFunctionList = [self.create_new_PIM, self.manipulate_existing_PIM, self.generate_personal_PIM_report,
                              self.load_PIM_file]
        self.ui.print_choose_hint("", "", moduleNameList)
        choice = self.ui.get_int_input(len(moduleNameList))
        while choice != 0:

            moduleFunctionList[choice - 1]()

            self.ui.print_down_line()

            self.ui.print_choose_hint("", "", moduleNameList)
            choice = self.ui.get_int_input(len(moduleNameList))

        # write user information into user file
        self._userManager.write_user_information()

    # ------------------------------------------------------------------------------------------------------------------------------

    # level 2: specific functional module
    def create_new_PIM(self):
        """1, create
    Output: add valid information -- add the PIM into system, print PIM information.  Option to exit midway: return directly
    Interaction process:
    (1) For now, just the basic interaction modes are performed: branch mode selection, linear message entry.
    More modes can be added later: e.g. group entry (entering multiple messages at once), e.g. entering different fields together. task name dealine ---"""
        self.ui.print_module_in("    Create new PIM.")

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

            fieldsMap = {}
            for field in fields:
                checker_function = checkersMap[field]

                if field == "start_time" or field == "deadline" or field == " reminder" or field == "alarms":
                    print(f"The expected format of {field}: YYYY-MM-DD HH:MM, e.g., 2023-10-18 14:00")

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
        """
        Discription:This function is for manipulating the PIRs, first, search the information,
                    then to choose to delete or modify them.
        :return None
        """
        self.ui.print_module_in("manipulate existing PIR")
        # 1, search module
        PIMList = self.search_PIM()
        if PIMList == None:
            return

        elif PIMList == []:
            self.ui.print_message("Cannot find the PIRs satisfying your criteria.")
            return

        # pre: get valid PIMList
        # 2, print the PIR
        self.ui.print_e_line()
        self.ui.print_message("The PIRs in your criteria in as follows: ")
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

            operation: delete or modify    +   index of the PIRs.

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
        """
        Discription: This funtion is to generate personal PIM report.
                    Users can choose to generate report for all PIMs or some specific PIMs.
        :return: None
        """

        # 1, print the information of PIMs
        self.ui.print_module_in("  Generate PIRs report.")

        PIMList = self._userManager.get_PIM_List()
        self.ui.print_message(f"You have {len(PIMList)} PIRs in total.")
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

        # 3, output
        self.ui.print_message(
            "Please specify the PIRs you want to print. (e.g., '1 2 3' to print PIR 1, 2, 3)Enter 0 to print all.)")
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
        """
        Description: This function is to load .pim file (which is generated by calling the above function) under
                    PIM/src/file/output/user_name/
        :return: None
        """
        # 1. print hint to load file
        self.ui.print_message("You can have these PIR files. Please choose one to load.")
        # 2. display all files that can be loaded
        IO(self._userManager).display_all_files()
        # 3. enter the file name (error message if not existed)
        file_name = input(self.ui.print_message("Please enter the file's name you want to load(.pim is not required):"))
        # 4. display the content of the pim file
        IO(self._userManager).load_file(file_name)

    # ------------------------------------------------------------------------------------------------------------------------------
    # level 3

    # 2, search
    # requirement description
    """
    As a user, I want to search for PIrs based on criteria concerning their types and the data stored in their fields. 
    whether the PIR belongs to a type. 
    whether a piece of text (stored in a note, a description, a name, an address, or a mobile number) contains a string, 
    whether a time (stored in a deadline, a starting time, or an alarm) is before (<), after (>), or equal to (=) another given point in time, 
    whether a condition combining multiple other conditions via logical connectors and (&&), or (||), and negation (!)
    """

    # interface
    """
    UserManager:
    self.__userManager.get_PIM_List() get all of the PIRs of the user. 

    PIM:
    contain_text()  # input: string  # output: True or False
    time_condition_checker(time:float, comparator: str)     # input: time, Comparison Symbols: < = >  # output： True or False
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
        then allow the user to input one line of the text to represent command:
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
        """
        This function is to search PIM according to a specific mode
        :return: List
        """
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

                    results = MainPage.compound_search(User, self._userManager.get_PIM_List(), condition)
                except Exception as e:
                    self.ui.print_message("Invalid input. Try again:")
                    continue
                break

        # Step 3: Return Results
        return results if results else []

    @staticmethod
    def check_alarms_or_reminders(User, PIMList):
        """
         Description:
        When the user logs in, tell the user the task that has passed the deadline and the event that has passed the start time,
        if it has not passed, but has passed the time set by alarm or reminder, remind the user.
        :param User:
        :param PIMList:
        :return: None
        """
        given_format = '%Y-%m-%d %H:%M'
        remind_lst = []
        coming_lst = []
        for pim in PIMList:
            task_type = User.PIM_type_to_class("task")
            event_type = User.PIM_type_to_class("event")
            remind_time, coming_time = None, None
            if isinstance(pim, task_type):
                remind_time = pim.get_reminder()
                coming_time = pim.get_deadline()

            elif isinstance(pim, event_type):
                remind_time = pim.get_alarms()
                coming_time = pim.get_start_time()

            if coming_time:
                current_timestamp = datetime.now().timestamp()
                coming_timestamp = datetime.strptime(coming_time.strip("'"), given_format).timestamp()
                if current_timestamp >= coming_timestamp:
                    coming_lst.append(pim)
                if remind_time:
                    remind_timestamp = datetime.strptime(remind_time.strip("'"), given_format).timestamp()
                    if remind_timestamp < current_timestamp < coming_timestamp:
                        remind_lst.append(pim)

        if len(coming_lst) != 0:
            print("These start times/ deadlines have passed:")
            for pim in coming_lst:
                print(f"{pim}\n")
        if len(remind_lst) != 0:
            print("There are some tasks/events you should remember:")
            for pim in remind_lst:
                print(f"{pim}\n")


    @staticmethod
    def compound_search(User, PIMList, condition):
        """
        Description: This function can do compound search based on multiple criteria.
        :param User:
        :param PIMList:
        :param condition:
        :return: List: search_result
        """
        condition = condition.strip()
        result = ""
        stack = []
        for i in range(len(condition)):
            char = condition[i]
            if char.isspace() or char.isalnum() or char in ["<", ">", "=", "-", ":", "!"]:
                result += char
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
                    input = request["time:"].strip()[1:].strip()
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
                result_lst.remove(condition1)
                result_lst[0] = condition1 + condition2
            elif condition == '&&':
                condition1 = result_lst[0]
                condition2 = result_lst[1]
                result_lst.remove(condition1)
                result_lst[0] = [value for value in condition1 if value in condition2]
            else:
                print("Invalid Expression")

        answer_lst = result_lst[0]
        return answer_lst

    # ------------------------------------------------------------------------------------------------------------------------------
    # 3, modify
    def modify_PIM(self, PIMList: List[PIM]):
        """
        Description:
        For each PIM, an interactive interface is provided for the user to indicate changes to the fields, enter new content, (validity checks, names need to be checked for duplicates).
        When finished, call the __userManager interface to make changes in the user information.
        :param PIMList: The PIM list that the user wants to modify
        :return: None
        """
        self.ui.print_e_line()
        self.ui.print_message(f"You have {len(PIMList)} to manipulate.")
        self.ui.print_message("Let's manipulate the PIRs now!")

        count = 0
        for pim in PIMList:
            # (1) print original infromation
            count += 1
            self.ui.print_message(f"\n---◅▯◊║◊▯▻  Round {count}  ◅▯◊║◊▯▻---\n"
                                  f"<--------- original --------->\n{pim}", )

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

                    while self._userManager.contains_name(input_field):
                        self.ui.print_message("The name already exist. please change another name.")
                        input_field = input()
                        if input_field in ['0', ""]:
                            break
                else:
                    field = fieldsList[choice - 1]

                    # 2' input new and check validity
                    self.ui.print_message(f"Enter the {field}")
                    input_field = newPim.get_field_input(field)

                    if not input_field:  # If no valid entry is made it means that the user wants to quit.
                        break

                # 3' change the field.
                newPim.__setattr__(field, input_field)

                # 4, next round
                self.ui.print_choose_hint("", "", fieldsList)
                choice = self.ui.get_int_input(len(fieldsList))

            # (3) print new inforamtion.
            self.ui.print_message(f"<--------- New Information After Manipulation -------->\n {newPim}")

            # (4) change in userManager
            self._userManager.modify(pim, newPim)

    # 4, delete
    def delete_PIM(self, PIMList: List[PIM]):
        """
        Description:
        This function is for deleting PIMs
        :param PIMList: The PIM that the user wants to delete
        :return: None
        """
        # 1, print the information of PIMs
        self.ui.print_e_line()
        print(f"You have {len(PIMList)} to delete.\n")
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
            self._userManager.delete(pim)

        # 4, print message
        self.ui.print_message("Delete successfully!")

