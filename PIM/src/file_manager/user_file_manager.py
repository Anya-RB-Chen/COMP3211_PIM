import os
import time
from PIM.src.model import *

class UserFileManager:
    __userFileRootPath = os.getcwd() + "/file" + "/user"


    def __init__(self, userFilePath):
        self.logInTimeStamp = time.time()
        self.__userFilePath = userFilePath

        if not os.path.exists(userFilePath):
            self.__create()
        self.__PIMList, self.__history = self.read()



    # mode: 0644. the file cannot be deleted by others.
    # the empty file should be able to be read correctly without errors.
    def __create(self):
        if not os.path.exists(self.__userFilePath):
            # 先不进行框架的print，因为在结束的write方法后，会把内容连同字段一起写入文件

            with open(self.__userFilePath, "w") as f:
                pass
            os.chmod(self.__userFilePath, 0o644)


    # interface:
    # 1, PIM.__str__ get the string output format of PIM type.   2, Tools.timeStamp_to_timeStr(timeStamp)
    # contents: 1, self.__PIMList pim list  2, previous log in/out time self.__history  + current log in time self.logInTimeStamp log out time: now.
    # output: PIMList list[PIM]  history list[[log_in_time_str, log_out_time_str]]

    def read(self):
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