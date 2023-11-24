import os

class OutputFileManager:
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
