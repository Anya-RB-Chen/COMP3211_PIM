import sys

sys.path.append("..")
from typing import List
from src.model.PIM import PIM
from src.tools.Tools import Tools



class Contact(PIM):


    def __init__(self, name: str, mobile_number: str, address: str = ""):
        super().__init__()
        self.name = name
        self.mobile_number = mobile_number
        self.address = address

    @classmethod
    def create(cls, name, fields_map):
        return cls(name, fields_map["mobile_number"], fields_map.get("address", ""))

    @classmethod
    def get_fields(cls) -> List[str]:
        return ["name", "mobile_number", "address"]

    @classmethod
    def get_explanation(cls):
        return "A contact is a person's information, including name, mobile numbers, and address."

    def get_fields_contents_map(self) -> dict:
        return {"name": self.name, "mobile_number": self.mobile_number, "address": self.address}

    @classmethod
    def get_fields_checkers_map(cls) -> dict:
        return {"name": lambda x: "" if x else "Name cannot be empty.",
                "mobile_number": Tools.check_mobile_number_format,
                "address": lambda x: ""}


    def contain_text(self, text: str):
        return text.lower() in self.name.lower() or text.lower() in self.mobile_number or text.lower() in self.address.lower()

    def __str__(self):
        return f"Name: {self.name}\nType: Contact\nMobile number: {self.mobile_number}\nAddress: {self.address}"


    def time_condition_checker(self, time: float, comparator: str):
        if comparator == "<":
            return time > self.createTime
        elif comparator == "=":
            return time == self.createTime
        elif comparator == ">":
            return time < self.createTime
        else:
            return False

    @classmethod
    def get_field_checker(cls, field: str):
        return cls.get_fields_checkers_map()[field]


    @classmethod
    def create_object_from_lines(cls, lines, index):

        name = Tools.get_value_from_line(lines[index])
        mobile_number = Tools.get_value_from_line(lines[index + 2])
        address = Tools.get_value_from_line(lines[index + 3])
        return cls(name, mobile_number, address)