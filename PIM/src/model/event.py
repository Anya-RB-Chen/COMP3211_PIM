from typing import List
import sys
sys.path.append("../..")
from model.pim import PIM
from tools.Tools import Tools


class Event(PIM):
    def __init__(self, name: str, description: str, start_time: str, alarms: str):
        super().__init__()
        self.name = name
        self.description = description
        self.start_time = start_time
        self.alarms = alarms if alarms else None

    def get_alarms(self):
        return self.alarms

    def get_start_time(self):
        return self.start_time

    @classmethod
    def create(cls, name, fields_map):
        return cls(name,fields_map["description"], fields_map["start_time"], fields_map.get("alarms", []))

    @classmethod
    def get_fields(cls) -> List[str]:
        return ["name", "description", "start_time", "alarms"]

    @classmethod
    def get_explanation(cls):
        return "An event is an occurrence that happens at a specific time and place, with a description and optional alarms."

    def get_fields_contents_map(self) -> dict:
        return {"name": self.name, "description": self.description, "start_time": self.start_time, "alarms": self.alarms}

    @classmethod
    def get_fields_checkers_map(cls) -> dict:
        return {"name": lambda x: "" if x else "Name cannot be empty.",
                "description": lambda x: "",
                "start_time": Tools.check_time_format,
                "alarms": Tools.check_time_format}

    def contain_text(self, text: str):
        return text.lower() in self.name.lower() or text.lower() in self.description.lower()

    def __str__(self):
        return f"Name: {self.name}\nType: Event\nDescription: {self.description}\nStart time: {self.start_time}\nAlarms: {self.alarms}"


    def time_condition_checker(self, time: float, comparator: str):
        if comparator == "<":
            return time > Tools.timeStr_to_timeStamp(self.start_time) or time > Tools.timeStr_to_timeStamp(self.alarms)
        elif comparator == "=":
            return time == Tools.timeStr_to_timeStamp(self.start_time) or time == Tools.timeStr_to_timeStamp(self.alarms)
        elif comparator == ">":
            return time < Tools.timeStr_to_timeStamp(self.start_time) or time < Tools.timeStr_to_timeStamp(self.alarms)
        else:
            return False

    @classmethod
    def get_field_checker(cls, field: str):
        return cls.get_fields_checkers_map()[field]

    @classmethod
    def create_object_from_lines(self, lines, index):
        name = Tools.get_value_from_line(lines[index])
        description = Tools.get_value_from_line(lines[index + 2])
        start_time = Tools.get_value_from_line(lines[index + 3])
        alarms = Tools.get_value_from_line(lines[index + 4])
        return Event(name, description, start_time, alarms)

