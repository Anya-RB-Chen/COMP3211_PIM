from PIM.src.model.PIM import PIM


class PlainText(PIM):
    def __init__(self, text="", name="unamed"):
        super().__init__(name)
        self.text = text

    @classmethod
    # text1 = PlainText.create("Shopping List", {"text": "Milk, Bread, Eggs, Butter"})
    def create(cls, name, fields_map):
        return cls(fields_map.get("text", ""), name)

    @classmethod
    def get_fields(cls) -> list[str]:
        return ["name", "text"]

    @classmethod
    def get_explanation(cls):
        return "A plain text is a simple text note with a name."

    def get_fields_contents_map(self) -> dict:
        return {"name": self.name, "text": self.text}

    @classmethod
    def get_fields_checkers_map(cls) -> dict:
        return {"name": lambda x: "" if x else "Name cannot be empty.",
                "text": lambda x: ""}

    def contain_text(self, text: str):
        return text.lower() in self.name.lower() or text.lower() in self.text.lower()

    def __str__(self):
        return f"Name: {self.name}\nType: PlainText\nText: {self.text}"

    def time_condition_checker(self, time: float, comparator: str):
        return False

    @classmethod
    def get_field_checker(cls, field: str):
        return cls.get_fields_checkers_map()[field]

