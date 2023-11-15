from typing import List
from PIM.src.model.PIM import PIM
from PIM.src.tools.Tools import Tools


class Task(PIM):
    def __init__(self, name, description, deadline, reminder=None):
        super().__init__()
        self.name = name
        self.description = description
        self.deadline = deadline
        self.reminder = reminder if reminder else ""

    def get_reminder(self):
        return self.reminder

    def get_deadline(self):
        return self.deadline

    @classmethod
    # task1 = Task.create("Buy groceries", {"description": "Buy milk, bread, and eggs", "deadline": "2023-10-25 19:00"})
    #        task2 = Task.create("Attend meeting",
    #                       {"description": "Team sync-up", "deadline": "2023-10-21 09:00", "reminder": "2023-10-20 09:00"})
    def create(cls, name, fields_map):
        return cls(name, fields_map["description"], fields_map["deadline"], fields_map.get("reminder", []))

    @classmethod
    def get_fields(cls) -> List[str]:
        return ["name", "description", "deadline", "reminder"]

    @classmethod
    def get_explanation(cls):
        return "A task is an activity that needs to be done, with a description, deadline, and optional reminders."

    def get_fields_contents_map(self) -> dict:
        return {"name": self.name, "description": self.description, "deadline": self.deadline, "reminder": self.reminder}

    @classmethod
    def get_fields_checkers_map(cls) -> dict:

        return {"name": lambda x: "" if x else "Name cannot be empty.",
                "description": lambda x: "" if x else "Description cannot be empty.",
                "deadline": Tools.check_time_format,
                "reminder": Tools.check_time_format}

    def contain_text(self, text: str):
        return text.lower() in self.name.lower() or text.lower() in self.description.lower()

    def __str__(self):
        # reminder_str = ", ".join(str(rem) for rem in self.reminder) if self.reminder else "None"
        return f"Name: {self.name}\nType: Task\nDescription: {self.description}\nDeadline: {self.deadline}\nReminder: {self.reminder}"

    def time_condition_checker(self, time: float, comparator: str):
        if comparator == "<":
            return time > Tools.timeStr_to_timeStamp(self.deadline)
        elif comparator == "=":
            return time ==  Tools.timeStr_to_timeStamp(self.deadline)
        elif comparator == ">":
            return time <  Tools.timeStr_to_timeStamp(self.deadline)
        else:
            return False

    @classmethod
    def get_field_checker(cls, field: str):
        return cls.get_fields_checkers_map()[field]

    @classmethod
    def create_object_from_lines(self, lines, index):
        name = Tools.get_value_from_line(lines[index ])
        description = Tools.get_value_from_line(lines[index + 2])
        deadline = Tools.get_value_from_line(lines[index + 3])
        reminder = Tools.get_value_from_line(lines[index + 4]) if lines[index + 4].strip().startswith("Reminder") else ""
        return Task(name, description, deadline, reminder)

