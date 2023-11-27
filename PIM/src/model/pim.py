from typing import List
from abc import abstractmethod, ABC
from time import time

from PIM.src.tools.InteractiveUI import InteractiveUI
from PIM.src.tools.Tools import Tools

class PIM:
    """
    This is the superclass for all specific PIMs.
    Please inherit this class if you want to add another PIM type.
    """

    def __init__(self):
        self.createTime = time()  # float

    def copy(self):
        """
        Create a new instance of the same class with the same name and fields
        :return:
        """
        fieldsMap = self.get_fields_contents_map()
        PIMType = type(self)
        return PIMType.create(self.name, fieldsMap)

    @classmethod
    @abstractmethod
    def create(cls, name, fieldsMap: dict):
        pass

    @classmethod
    @abstractmethod
    def decode(cls):
        """For categories to be described. Basic functions, fields."""
        pass

    @classmethod
    @abstractmethod
    def get_fields(cls) -> List[str]:
        """Get the fields of the PIM class, represented as a list of strings."""
        pass

    @classmethod
    @abstractmethod
    def get_fields_checkers_map(cls) -> dict:
        """
        Get checker functions to determine the validity of different fields.
        checker methods Input field content, output error message or "" means that the field conforms to the format specification.
        """
        pass

    @classmethod
    @abstractmethod
    def get_explaination(cls):
        """
        For categories to be described. Basic functions, fields.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def get_fields_contents_map(self) -> dict:
        """fields -> content map"""
        pass

    @abstractmethod
    def contain_text(self, text: str):
        pass

    @abstractmethod
    def time_condition_checker(self, time: float, comparator: str):
        """
        :param time: timestamp
        :param comparator: comparison symbols: limit < = > three
        :return: boolean
        """
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
    def get_field_input(cls, field: str):
        """
        This function is to get a valid input of field
        :param field: input field
        :return: None
        """

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
        return input_field
