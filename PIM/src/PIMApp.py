import os
import traceback

from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.MainPage import MainPage
from PIM.src.module.SystemManager import SystemManager,UserProfile
from PIM.src.tools.Tools import Tools
from module.CMDLineIntepreter import CMDLineIntepreter
from module.UserManager import UserInformationManager
from module.Logger import Logger


# 10.14 1h 自顶向下 XP实现。
# User story. no -- 用流程图
# 直接面向过程，自顶向下面向对象搭建。

# 对于面向过程的设计，依然用对象的方式实现，毕竟这样可以实现多线程，多用户同时用一个程序登录。 虽然者没什么用
# 如果设计模式不好，等着改掉。现在没时间研究这些细节。
class PIMApp:


    # level 0
    __logFilePath =  os.getcwd() + "/file" + "/log" + "/log.txt"


    def __init__(self): # 先不用单例模式。直接把系统文件作为字段来使用。
        # file system initialization
        self.file_system_initialization()

       # 系统模块初始化
        self.systemManager = SystemManager()
        self.logger = Logger(PIMApp.__logFilePath)

       # ------------------------------------------------------------------------------------------------------------------------------
       # 测试
       #  self.systemManager.add_profile(UserProfile("Mike", "123456", "21100038d@connect.polyu.hk", "hhh"))
       # ------------------------------------------------------------------------------------------------------------------------------
        self.mainPage = MainPage()
        self.cmdIntepreter = CMDLineIntepreter()


    # level 0 : 自顶向下开发， 设计 - 开发 - 建模 三部分同步，形成高效信息循环。按照实际场景做建模，根据模型做设计，根据设计做开发。
    # 即时性的反馈 +  系统性的开发方法。

    def main(self):
        ui = InteractiveUI()
        # 1, welcome message and hint.
        ui.print_welcome_message()

        # ------------------------------------------------------------------------------------------------------------------------------
        if len(self.systemManager.get_user_profiles()) == 0:
            print("测试模式: 添加新用户 Mike")
            testUserProfile = UserProfile("Mike", "123456", "","")
            self.systemManager.add_profile(testUserProfile)
            self.systemManager.system_file_write()
            # print( "以默认用户Mike方式登录", testUserProfile)
            # self.mainPage.main(testUserProfile)

        # ------------------------------------------------------------------------------------------------------------------------------


        # 2, page 1: log in system | register | command mode
        choice = " \n直接输入4以默认用户Mike登录，跳过log in module  \n1 --log in  2 --register 3--command mode.0-- quit"
        ui.print_choose_hint("","",choice)

        choice = ui.get_int_input(3 + 1) #

        # 2, 
        try:
            if choice == 1: # 登录 -- 进入系统
                userProfile = self.login()
                if userProfile:
                    self.mainPage.main(userProfile)

                    
            elif choice == 2: #注册 -- 进入系统
                userProfile = self.register()
                if UserProfile:
                    ui.print_choose_hint("","Do you want to log in directly?", "1-- yes")
                    choice1 = ui.get_int_input(1)
                    if choice1:
                        self.mainPage.main(userProfile)
        
            elif choice == 3: # cmd模式。 需要改交互方式。 这只作为一个 prototype
                self.cmdLineMode()

            elif choice == 4: # 测试模式
                defaultUserProfile = self.systemManager.get_user_profiles()[0]
                print( "以默认用户Mike方式登录",)
                self.mainPage.main(defaultUserProfile)

                
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
        UserInformationManager.set_output_file_root_path(outputRootPath)

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
            # ------------------------------------------------------------------------------------------------------------------------------
            self.systemManager.system_file_write()
            # ------------------------------------------------------------------------------------------------------------------------------

            return user_profile

# ------------------------------------------------------------------------------------------------------------------------------
    # 拓展功能 -- 留存
    
    def cmdLineMode(self):
        pass
 # ------------------------------------------------------------------------------------------------------------------------------
    
    # clear the resource of system
    def system_clear_up(self):
        pass





if __name__ == "__main__":
    app = PIMApp()
    app.main()


