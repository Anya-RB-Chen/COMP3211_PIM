import datetime
import random
import re
from enum import Enum
from datetime import datetime, timezone


class InputType(Enum):
    COMPARATOR = "comparator"
    TIME = "time"
    EMAIL = "email"
    PIMTYPE = "pim type"
    MOBILE_NUMBER = "mobile_number"


class Tools:
    @staticmethod
    def checkNameAvailable(name: str) -> bool:
        """
        Check if the given name is valid.

        A valid name should:
        - contain only letters, digits, and underscores
        - start with a letter
        - have at least 3 characters and at most 20 characters

        Args:
            name (str): The name to check.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if not name.isidentifier():
            return False
        if len(name) < 3 or len(name) > 20:
            print("Your username must be between 3 and 20 characters in length")
            return False
        return True

    @staticmethod
    def checkPasswordStrength(password: str) -> bool:
        """
        Check if the given password is strong enough.

        A strong password should:
        - have at least 8 characters
        - contain at least one uppercase letter, one lowercase letter, one digit, and one special character

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password is strong enough, False otherwise.
        """
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char in "!@#$%^&*()-_=+[]{}\\|;:'\",.<>/?`~" for char in password):
            return False
        return True

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validates whether a given string is a well-formed email address.

        Correct Email Standard:
        1. Begins with an alphanumeric character.
        2. Can contain periods, hyphens, and underscores.
        3. Contains an @ symbol.
        4. After the @ symbol, contains an alphanumeric domain name followed by a period.
        5. Ends with a domain suffix like "com", "org", "net", etc.

        Args:
        - email (str): The email string to validate.

        Returns:
        - bool: True if email is valid, False otherwise.

        Examples:
        # >>> is_valid_email("example.email@domain.com")
        True

        # >>> is_valid_email("invalid_email@domain")
        False

        # >>> is_valid_email("another.invalid_email@.com")
        False
        """
        # Split the email at '@' and ensure there are only 2 parts
        parts = email.split('@')
        if len(parts) != 2:
            return False

        local, domain = parts

        # Check the local part for allowed characters
        if not all(c.isalnum() or c in ['.', '-', '_'] for c in local):
            return False

        # Split domain into name and suffix
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            return False

        domain_name, domain_suffix = domain_parts[0], domain_parts[-1]

        # Ensure domain name and suffix are alphanumeric
        if not domain_name.isalnum() or not domain_suffix.isalpha():
            return False

        return True

    # ------------------------------------------------------------------------------------------------------------------------------
    # 格式检验函数：

    # 输入： 字符串，   输出：【正确】空字符串   【错误】 正确格式的提示
    @staticmethod
    def check_time_format(str) -> str:
        format_string = "%Y-%m-%d %H:%M"
        # Regular expression to match the desired format
        pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"
        if re.match(pattern, str):
            try:
                datetime.strptime(str, format_string)
                return ""
            except ValueError:

                return ("Your input is not in the correct time format. Expected format: YYYY-MM-DD HH:MM, e.g., "
                        "2023-10-18 14:00.")

            return ""

        else:
            return "Expected format: YYYY-MM-DD HH:MM, e.g., 2023-10-18 14:00"

    @staticmethod
    def check_comparator_format(str) -> str:
        valid_comparators = ['<', '=', '>']
        if str in valid_comparators:
            return ""
        else:
            return "Expected one of the following comparators: <, =, >"

    @staticmethod
    def check_PIM_type_format(str) -> str:
        str = str.lower()
        valid_types = ['task', 'plaintext', 'event', 'contact']
        if str in valid_types:
            return ""
        else:
            return "Expected one of the following PIM types: Task, PlainText, Event, Contact"

    @classmethod
    def check_email_format(cls, email):
        if Tools.is_valid_email(email):
            return ""
        else:
            return "Invalid format. Expected a valid email format, e.g., example@example.com"

    @classmethod
    def check_mobile_number_format(cls, mobileNumber):
        if all(num.isdigit() for num in mobileNumber):
            return ""
        if all(num.isdigit() or num == '-' for num in mobileNumber) and mobileNumber.count('-') == 2:
            return ""
        else:
            return "Mobile numbers should only contain digits and be in the format '123-456-7890'."

    @staticmethod
    def get_type_format_checker(inputType):
        type_checker_map = {
            InputType.COMPARATOR: Tools.check_comparator_format,
            InputType.TIME: Tools.check_time_format,
            InputType.EMAIL: Tools.check_email_format,
            InputType.PIMTYPE: Tools.check_PIM_type_format,
            InputType.MOBILE_NUMBER: Tools.check_mobile_number_format
        }

        if isinstance(inputType, InputType):
            if inputType in type_checker_map:
                return type_checker_map[inputType]
            return None

        typeStr_checker_map = {
            "comparator": Tools.check_comparator_format,
            "time": Tools.check_time_format,
            "email": Tools.check_email_format,
            "pimtype": Tools.check_PIM_type_format
        }
        if isinstance(inputType, str):
            inputType = inputType.lower()
            if inputType in typeStr_checker_map:
                return typeStr_checker_map[inputType]
            return None

        return None

    # def validate_format_correctness(input_type: InputType, value: str) -> str:
    #     type_checker_map = {
    #         InputType.COMPARATOR:Tools.check_comparator_format,
    #         InputType.TIME: Tools.check_time_format,
    #         InputType.EMAIL:  Tools.check_email_format,
    #         InputType.PIMTYPE: Tools.check_PIM_type_format
    #     }
    #     if input_type in type_checker_map:
    #         return type_checker_map[input_type](value)
    #     else:
    #         return "Unknown input type"

    # ------------------------------------------------------------------------------------------------------------------------------
    # 时间性质
    @staticmethod
    def timeStr_to_timeStamp(time_str: str) -> int:
        """
        Convert datetime string in format "YYYY-MM-DD HH:MM" to UNIX timestamp.
        """
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        return int(dt.replace(tzinfo=timezone.utc).timestamp())

    @staticmethod
    def timeStamp_to_timeStr(timestamp: float) -> str:
        """
        Convert UNIX timestamp to datetime string in format "YYYY-MM-DD HH:MM".
        """
        dt = datetime.utcfromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")

    # 文件I/O
    @staticmethod
    def get_value_from_line(line):
        index = line.index(":")
        return line[index + 1:].strip()

    def check_alarms_or_reminders(User, PIMList):
        given_format = '%Y-%m-%d %H:%M'

        # given_timestamp = datetime.strptime(time, given_format).timestamp()  # 解析给定日期和时间，并转换为时间戳
        current_timestamp = datetime.now().timestamp()  # 获取当前时间戳

        num = 0
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

            if remind_time:
                remind_timestamp = datetime.strptime(remind_time.strip("'"), given_format).timestamp()
                coming_timestamp = datetime.strptime(coming_time.strip("'"), given_format).timestamp()
                current_timestamp = datetime.now().timestamp()  # 获取当前时间戳
                if remind_timestamp < current_timestamp < coming_timestamp:
                    num += 1
                    if num == 1:
                        print("there are some tasks/events you should remember:")
                    print(f"{pim}\n")

    @staticmethod
    def compound_search(User, PIMList, condition):
        result = ""
        stack = []
        for i in range(len(condition)):
            char = condition[i]
            if char.isspace() or char.isalnum() or char in ["<", ">", "=", "-", ":"]:
                result += char
            elif char == "(":
                stack.append(char)
            elif char == ")":
                result += " "
                while (len(stack) != 0) and (stack[-1] != "("):
                    result += stack.pop()
                    if len(stack) != 0:
                        if result[-1] == "!":
                            result += " "
                stack.pop()
            else:
                stack.append(char)

        result += " "
        while len(stack) != 0:
            if stack[-1] == "(": return "Invalid Expression"
            result += stack.pop()
            if len(stack) != 0:
                if result[-1] == "!":
                    result += " "

        handle = result.split(" ")
        handle2 = []
        for j in handle:
            if len(j) != 0:
                handle2.append(j)

        compound_lst = [char for char in handle2 if char in ["||", "&&", "!"]]
        handle2 = [char for char in handle2 if char not in ["||", "&&", "!"]]

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
            if "type" in request.keys():
                inputStr = request["type"]
                pim_type = User.PIM_type_to_class(inputStr)
                results = [pim for pim in PIMList if isinstance(pim, pim_type)]
                result_lst.append(results)
            if "text" in request.keys():
                results = [pim for pim in PIMList if pim.contain_text(request["text"])]
                result_lst.append(results)
            if "time" in request.keys():
                input = request["time"]
                comparator = request[1]
                time_input = input[1:].strip()
                timestamp = Tools.timeStr_to_timeStamp(time_input)

                results = [pim for pim in PIMList if pim.time_condition_checker(timestamp, comparator)]
                result_lst.append(results)

        answer_lst = []
        for condition in compound_lst:
            if condition == "!":
                template = result_lst[-1]
                result_lst[-1] = [pim for pim in PIMList if pim not in template]
            elif condition == "||":
                condition1 = result_lst[-1]
                condition2 = result_lst[-2]
                result_lst.pop()
                result_lst.pop()
                result_lst.append([pim for pim in (condition1 or condition2)])
            elif condition == "&&":
                condition1 = result_lst[-1]
                condition2 = result_lst[-2]
                result_lst.pop()
                result_lst.pop()
                result_lst.append([pim for pim in (condition1 and condition2)])
            else:
                print("Invalid Expression")

        answer_lst = result_lst[0]
        return answer_lst


# print(Tools.compound_in_to_pro(
#     "type: Task && (text: abc  || (time: < 2023-10-18 14:00 || time: ! > 2023-12-12 12:00))"))
