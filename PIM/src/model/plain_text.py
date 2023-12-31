from typing import List
from PIM.src.model.pim import PIM
from PIM.src.tools.Tools import Tools


class PlainText(PIM):
    """
    This class is the Plain test type. It inherits the PIM class.
    Two properties: name, text.
    """
    def __init__(self, name, text=""):
        super().__init__()
        self.name = name
        self.text = text

    @classmethod
    def create(cls, name, fields_map):
        return cls(name,fields_map.get("text", ""))

    @classmethod
    def get_fields(cls) -> List[str]:
        return ["name", "text"]

    @classmethod
    def get_explanation(cls):
        return "A plain text is a simple text note with a name."

    def get_fields_contents_map(self) -> dict:
        return {"name": self.name, "text": self.text}

    @classmethod
    def get_fields_checkers_map(cls) -> dict:
        return {"name": lambda x: "",
                "text": lambda x: "" if x else "text cannot be empty."}

    def contain_text(self, text: str):
        return text.lower() in self.name.lower() or text.lower() in self.text.lower()

    def __str__(self):
        return f"Name: {self.name}\nType: PlainText\nText: {self.text}"

    def time_condition_checker(self, time: float, comparator: str):
        return False

    @classmethod
    def get_field_checker(cls, field: str):
        return cls.get_fields_checkers_map()[field]

    @classmethod
    def create_object_from_lines(self, lines, index):
        name = Tools.get_value_from_line(lines[index ])
        text = Tools.get_value_from_line(lines[index + 2])
        return PlainText(name, text)

