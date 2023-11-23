import unittest
import sys
sys.path.append("..")
from PIM.src.model.plain_text import PlainText


class PlainTextTests(unittest.TestCase):
    def test_create(self):
        name = "Shopping List"
        fields_map = {"text": "Milk, Bread, Eggs, Butter"}
        plain_text = PlainText.create(name, fields_map)
        self.assertEqual(plain_text.name, name)
        self.assertEqual(plain_text.text, fields_map["text"])

    def test_get_fields(self):
        expected_fields = ["name", "text"]
        self.assertEqual(PlainText.get_fields(), expected_fields)

    def test_get_explanation(self):
        expected_explanation = "A plain text is a simple text note with a name."
        self.assertEqual(PlainText.get_explanation(), expected_explanation)

    def test_get_fields_contents_map(self):
        name = "Shopping List"
        text = "Milk, Bread, Eggs, Butter"
        plain_text = PlainText(name, text)
        expected_contents_map = {"name": name, "text": text}
        self.assertEqual(plain_text.get_fields_contents_map(), expected_contents_map)

    def test_contain_text(self):
        name = "Shopping List"
        text = "Milk, Bread, Eggs, Butter"
        plain_text = PlainText(name, text)
        self.assertTrue(plain_text.contain_text("Milk"))
        self.assertTrue(plain_text.contain_text("bread"))
        self.assertFalse(plain_text.contain_text("Cheese"))

    def test_to_string(self):
        name = "Shopping List"
        text = "Milk, Bread, Eggs, Butter"
        plain_text = PlainText(name, text)
        expected_string = f"Name: {name}\nType: PlainText\nText: {text}"
        self.assertEqual(str(plain_text), expected_string)

    def test_time_condition_checker(self):
        name = "Shopping List"
        text = "Milk, Bread, Eggs, Butter"
        plain_text = PlainText(name, text)
        self.assertFalse(plain_text.time_condition_checker(0.0, "<"))

    def test_get_field_checker(self):
        name_checker = PlainText.get_field_checker("name")
        text_checker = PlainText.get_field_checker("text")
        self.assertTrue(callable(name_checker))
        self.assertTrue(callable(text_checker))

    def test_create_object_from_lines(self):
        lines = [
            "Name: Shopping List",
            "Type: PlainText",
            "Text: Milk, Bread, Eggs, Butter",
            "-------------------"
        ]
        index = 0
        expected_name = "Shopping List"
        expected_text = "Milk, Bread, Eggs, Butter"
        plain_text = PlainText.create_object_from_lines(lines, index)
        self.assertEqual(plain_text.name, expected_name)
        self.assertEqual(plain_text.text, expected_text)


if __name__ == "__main__":
    unittest.main()