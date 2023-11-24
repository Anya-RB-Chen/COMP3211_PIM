import sys

sys.path.append("..")
from typing import List
from abc import abstractmethod,ABC
from time import time

from src.tools.InteractiveUI import InteractiveUI
from src.tools.Tools import Tools



class PIM:

    # field : 通用字段只有时间？？
    def __init__(self):
        self.createTime = time()  # float 时间戳
        #self.name = name    # 名称被视作字段？


    def copy(self):
    # Create a new instance of the same class with the same name and fields
        fieldsMap =  self.get_fields_contents_map()
        PIMType = type(self)
        return PIMType.create(self.name,fieldsMap)


    # 自顶向下开发， 接口与实现统一。
    # 在进行上层功能模块实现时，同步对于下层接口进行定义。 注意不同情况，限制条件。 先开发上层 + 设计下层接口 再开发下层方法 -- XP策略一种实行？ 信息循环？
    # 在最适合做设计的时间进行设计，在有合理设计的基础上再做开发。 节省设计时空想的时间，设计与实际不匹配方向有误，或者开发陷入混乱。 既打通信息循环又能够 保持high level视角


    # 根据名称和字段 -- 内容哈希表 创建新对象。
    @classmethod
    @abstractmethod
    def create(cls,name, fieldsMap: dict):
        pass

    @classmethod
    @abstractmethod
    # 对于类别进行描述。 基本功能，字段。
    def decode(cls,):
        pass

    @classmethod
    @abstractmethod
    # 得到PIM类的字段，用字符串列表表示。
    def get_fields(cls) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    # 得到判断不同字段有效性的检验函数。
    # checker methods 输入字段内容，输出错误提示信息 或者 "" 表示字段符合格式规范。
    def get_fields_checkers_map(cls) -> dict:
        pass

    @classmethod
    @abstractmethod
    # 对于类别进行描述。 基本功能，字段。
    def get_explaination(cls):
        pass

    # ------------------------------------------------------------------------------------------------------------------------------


    @abstractmethod
    # fields -> content map
    def get_fields_contents_map(self) -> dict:
        pass


    @abstractmethod
    def contain_text(self, text: str):
        pass

    @abstractmethod
    # 输入： 时间戳，比较符号： 限制 < = > 三种
    # 输出： True or False
    def time_condition_checker(self, time: float, comparator: str):
        pass


    @abstractmethod
    def __str__(self):
        pass

    @classmethod
    @abstractmethod
    def get_field_checker(cls, field: str):
        pass


    @classmethod
    @abstractmethod
    def create_object_from_lines(self, lines, index):
        pass

    @classmethod
    # get a valid input of field  |  None
    def get_field_input(cls, field: str):
    # if field == "name": # assumption：
    ## 对于名字唯一的限制是不可以重复, 在外部执行逻辑，因为名字重复属于PIMList User information 已经超越了PIM类方法的范畴。
    #     name = input()
    #     while name not in ["", "0"]:
    #         if
        checker = cls.get_field_checker(field)

        input_field = input()
        if not input_field:
            return None

        wrongMessage = checker(input_field)
        while input_field not in ["", "0"] and wrongMessage != "":
            InteractiveUI._instance.print_message(f"Invalid format. {wrongMessage}")
            InteractiveUI._instance.print_message(("Please input again: "))

            input_field = input()
            if input_field in ["", "0"]:
                return None
            wrongMessage = checker(input_field)

    # type conversion
    # if time -> change to float.
    # zwx: 如果要比较时间的话单独写个时间比较函数
    # if Tools.check_time_format(input_field) == "":
    #     return Tools.timeStr_to_timeStamp(input_field)

    # other field needing change format ?
        return input_field


