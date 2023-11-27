import os
import time
import random

from colorama import Fore

from PIM.src.tools.Tools import InputType, Tools


# create the global instance for the interactive UI



class InteractiveUI:
    _instance = None

    LEN = 200
    HALF_COLUMN = 50

    def __new__(cls):

        if not cls._instance:
            cls._instance = super(InteractiveUI, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            # Try to get the size of the terminal
            self.rows, self.columns = os.get_terminal_size(0)
        except:
            # Default size if unable to fetch terminal size
            self.rows, self.columns = 24, 80

        InteractiveUI.LEN = self.columns * 2
        InteractiveUI.HALF_COLUMN = self.columns // 2
        pass

# ------------------------------------------------------------------------------------------------------------------------------
    # color property
    COLORS = [
        Fore.RED,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.CYAN,  # Used as an approximation for Blue
        Fore.BLUE,  # Used as an approximation for Indigo
        Fore.MAGENTA,  # Used as an approximation for Violet
        Fore.WHITE
    ]

    @staticmethod
    def random_color():
        return random.choice(InteractiveUI.COLORS)

    def get_random_color_words(self, message):
        colored_message = " ".join([self.random_color() + word for word in message.split(" ")])
        return colored_message

    def get_random_color_sentence(self, message):
        colored_message = "\n".join([self.random_color() + word for word in message.split("\n")])
        return colored_message

    def get_rainbow_color_sentence(self, message):
        sentences = message.split("\n")
        colored_message = []

        # Use a for loop with an index so we can cycle through the colors
        for i, word in enumerate(sentences):
            color = InteractiveUI.COLORS[i % len(InteractiveUI.COLORS)]
            colored_message.append(color + word + Fore.RESET)

        return "\n".join(colored_message)

    # @staticmethod 可以尝试换成静态方法或者类方法。
    def print_leave_message(self):
        hint = """
             ●●●●●●●●●●      ●●●        ●●●  ●●●●●●●●●●●       ▮▮▮▮▮
             ●●●●●●●●●●●       ●●      ●●    ●●●●●●●●●●●       ▮▮▮▮▮
             ●●       ●●        ●●●   ●●●    ●●                ▮▮▮▮▮
             ●●       ●●          ●●●●●      ●●                ▮▮▮▮▮
             ●●      ●●●           ●●●       ●●                ▮▮▮▮▮
             ●●●●●●●●●●            ●●●       ●●●●●●●●●●●       ▮▮▮▮▮
             ●●●●●●●●●●●           ●●●       ●●●●●●●●●●●       ▮▮▮▮▮
             ●●       ●●           ●●●       ●●                ▮▮▮▮▮
             ●●        ●●          ●●●       ●●
             ●●      ●●●●          ●●●       ●●                 ◍◍◍
             ●●●●●●●●●●●           ●●●       ●●●●●●●●●●●       ◍◍◍◍◍
             ●●●●●●●●●             ●●●       ●●●●●●●●●●●        ◍◍◍
         """
        hint = "".join([self.random_color() + char for char in hint])
        self.print_at_center(hint)
        time.sleep(1)




    def print_welcome_message(self):
        hint = """
          ◇◇◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◇
        ◇◇                                                                            ◇◇◇
       ◇◇         ▥          ▥        ▥           ▥         ▥        ▥       ▥          ◇◇◇
     ◇◇ ┌──────────────────────────────────────────────────────────────────────────――─┐    ◇◇
    ◇◇  ┼                                                                             │     ◇◇
        │ ●     ●●      ●  ●●●●●●●  ●           ●●●●    ●●●●     ●     ●      ●●●●●●  │       Λ
   Λ    │ ●●    ●●●    ●●  ●        ●         ●●●      ●●  ●●    ●●●  ●●●     ●       │      ╱ ╲
  ╱ ╲   │  ●●   ● ●●   ●●  ●●●●●●●  ●        ●●       ●●    ●●  ●● ●●●● ●●    ●●●●●●  │     ▕   ▏
 ▕   ▏  │   ●● ●●  ●● ●●   ●        ●        ●●       ●●    ●●  ●●  ●●●  ●●   ●       │      ╲ ╱
  ╲ ╱   │    ●●●    ●●●●   ●        ●        ●●●      ●●    ●● ●●   ●●    ●●  ●       │       V
   V    │     ●●      ●    ●●●●●●●  ●●●●●●●    ●●●●●    ●●●●   ●     ●     ●  ●●●●●●  │
        │                                                                             │    ◇◇
   ◇◇   └───────────────────────────────────────────────────────────────────────────――┘  ◇◇◇
    ◇◇◇          ▥          ▥         ▥       ▥                ▥      ▥       ▥         ◇◇◇
       ◇◇◇                                                                            ◇◇
         ◇◇◇◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌◌
         """
        hint = "".join([self.random_color() + char for char in hint])
        self.print_at_center(hint)

        time.sleep(1)

    def print_leave_main_page(self):
        mainPageOut = "                                                                                                                                                                  \n" + \
                        "●         ●●●●●●     ●●     ●      ●   ●●●●●●               ●●●●●●     ●●        ●●●●   ●●●●●●           \n" + \
                        "●         ●          ●●     ●●    ●●   ●                    ●    ●     ●●       ●●      ●                \n" + \
                        "●         ●●●●●●    ●  ●     ●   ●●    ●●●●●●               ●●●●●●    ●  ●     ●●       ●●●●●●           \n" + \
                        "●         ●        ●●●●●●    ●● ●●     ●                    ●        ●●●●●●    ●   ●●   ●                \n" + \
                        "●         ●       ●●    ●     ●●●      ●                    ●       ●●    ●●   ●●  ●●   ●                \n" + \
                        "●●●●●●●   ●●●●●●  ●     ●      ●●      ●●●●●●               ●       ●     ●●   ●●●●●●   ●●●●●●           "
        self.print_at_center(self.random_color() + mainPageOut)


    def print_module_in(self,module_name):
        # 3 lines
        print("\n")
        s = " " * 45  # Equivalent to the Java string with 57 spaces
        s1 = s.replace(" ", " ")
        s2 = "▾" * 137  # Creates a string with 137 "▾" characters
        s2 = s2.replace("▾", " ")

        # Constructing and printing the message
        print(Fore.YELLOW + f"{s}   ╔━━━━━━━━━━━━━━━━━━━━━━╗\n{s1}   ║   ▿   ▿   ◈   ▿   ▿  ║ ")
        print(Fore.YELLOW + f"{s}    {module_name}")
        print(Fore.YELLOW + f"{s1}   ║   ▿   ▿   ◈   ▿   ▿  ║   \n{s}   ╚━━━━━━━━━━━━━━━━━━━━━━╝\n")


    def print_module_out(self, module_name):
        print(f"\nLeave {module_name}")
        self.print_line()

    def get_int_input(self,n):
        while True:
            try:
                num = int(input(f"Enter an integer from 0 to {n}: "))
                if 0 <= num <= n:
                    return num
                else:
                    print("Invalid input, please try again")
            except ValueError:
                print("Invalid input, please try again")

    def get_int_input_list(self, n):
        while True:
            try:
                li = list(map(int, input(f"Enter integers from 0 to {n}: ").split()))
                for i in range(len(li)):
                    num = li[i]
                    while num < 0 or num > n:
                        print(f"{num} in an invalid input. Please try again")
                        num = self.get_int_input(n)
                    li[i] = num
                return sorted(list(set(li)))

            except Exception:
                print("Invalid input, please try again")


    def print_line(self):
        print(Fore.RED + "-" * self.LEN)

    def get_n_char(self, char, n):
        return char * n

    def print_choose_hint(self, name, description, choice):

        if name:
            s1 = self.get_n_char("◦", self.HALF_COLUMN) + f"  {name}  " + self.get_n_char("◦", self.HALF_COLUMN)
            print(s1[:self.LEN])

        if description:
            s2 = self.get_n_char("-", self.HALF_COLUMN) + f"  {description}  " + self.get_n_char("-", self.HALF_COLUMN)
            print(s2[:self.LEN])

        if choice:
            if isinstance(choice, list):
                buffer = []
                length = len(choice)
                for i in range(length):
                    buffer.append("%d--" % (i + 1) )
                    buffer.append(choice[i] + " ")
                choice = "".join(buffer)

            print( f"Enter an integer to make the choose (enter 0 to quit): {choice}")


    def print_message(self, hint):
        # Split the message into characters and colorize each one
        print(self.get_rainbow_color_sentence(hint))

    def input_hint(self, hint):
        colored_hint = Fore.BLUE + hint
        return input(colored_hint)


    def print_user_welcome_message(self, name):
        print("\n\n")
        print(self.get_n_char("◌", self.LEN))

        s = "  ------ ◅▯◊║◊▯▻    Hi, " + name + ".  Welcome to PIM system.   ◅▯◊║◊▯▻  -------"
        self.print_at_center(self.random_color() +s)

        print(self.random_color() + self.get_n_char("◌", self.LEN))

    def print_down_line(self):
        print(self.random_color() +self.get_n_char("▴", self.LEN))
        print(self.random_color() +self.get_n_char("◌", self.LEN))

    def print_e_line(self):
        print(self.get_n_char("▾", self.LEN))

    def print_main_page(self):
        # Get the size of the terminal

        # Create the MAIN Page message box
        message = """
         ☆──────────✬❖✬──────────☆
         │       ❈❈❈❈❈❈❈❈❈❈      │
         │       ❈  MAIN  ❈      │
         │       ❈  Page  ❈      │
         │       ❈❈❈❈❈❈❈❈❈❈      │
         ☆──────────✬❖✬──────────☆

        """



     ## 输入 类型
    # 输出： 正确格式的相应类型字符串 或者空字符串 （不想继续输入） 进行交互，但是不提供输入提示
    ### 需不需要定义推出逻辑还需要继续想。 因为有的字段允许空白输入。 ### 需不需要定义推出逻辑还需要继续想。 因为有的字段允许空白输入。
    ### 这部分与PIM的get field input 重复。 对于格式检验与有效输入的这部分逻辑，需要统一做调整。  看所有的接口调用，整合逻辑，清晰的方式定义接口。

    def get_correct_input(self, inputType: InputType) -> str:
        inputFormatChecker = Tools.get_type_format_checker(inputType)

        typeName = inputType
        inputStr = input()
        # if inputStr == "0":
        #     return ""
        wrongMessage = inputFormatChecker(inputStr)

        while wrongMessage:
            self._instance.print_message(f"Incorrect format.\n"
                                        f"{wrongMessage}")
            inputStr =  self._instance.input_hint(f"Enter again: ")
            # if not inputStr or inputStr == "0":
            #     return ""
            wrongMessage = inputFormatChecker(inputStr)

        return inputStr

    def print_at_center(self, message):
        # Split the message into lines
        lines = message.split("\n")

        # Calculate the padding for centering
        # total_length = max(len(line) for line in lines) + self.columns
        # left_padding = (self.columns - total_length) // 2

        # Print each line of the message with the padding
        for line in lines:
            print(" " * int(self.HALF_COLUMN) + line)

#
# ui = InteractiveUI()
# ui.print_module_in("module")


