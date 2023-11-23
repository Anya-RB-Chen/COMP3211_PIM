import unittest
import sys
sys.path.append("..")
from PIM.src.model.task import Task


class TaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = Task("Buy groceries","Buy milk, bread, and eggs","2023-10-25 19:00", "2023-10-20 09:00")

    def test_create(self):
        name = "Buy groceries"
        fields_map = {
            "description": "Buy milk, bread, and eggs",
            "deadline": "2023-10-25 19:00"
        }
        task = Task.create(name, fields_map)
        self.assertEqual(task.name, name)
        self.assertEqual(task.description, fields_map["description"])
        self.assertEqual(task.deadline, fields_map["deadline"])
        self.assertEqual(task.reminder, "")

        name = "Attend meeting"
        fields_map = {
            "description": "Team sync-up",
            "deadline": "2023-10-21 09:00",
            "reminder": "2023-10-20 09:00"
        }
        self.assertNotEqual(task.name, name)
        self.assertNotEqual(task.description, fields_map["description"])
        self.assertNotEqual(task.deadline, fields_map["deadline"])
        self.assertNotEqual(task.reminder, fields_map["reminder"])

    def test_get_fields(self):
        expected_fields = ["name", "description", "deadline", "reminder"]
        self.assertEqual(Task.get_fields(), expected_fields)

    def test_get_explanation(self):
        expected_explanation = "A task is an activity that needs to be done, with a description, deadline, and optional reminders."
        self.assertEqual(Task.get_explanation(), expected_explanation)

    def test_get_fields_contents_map(self):
        name = "Buy groceries"
        description = "Buy milk, bread, and eggs"
        deadline = "2023-10-25 19:00"
        reminder = "2023-10-20 09:00"
        task = Task(name, description, deadline,reminder)
        expected_contents_map = {
            "name": name,
            "description": description,
            "deadline": deadline,
            "reminder": reminder
        }
        self.assertEqual(task.get_fields_contents_map(), expected_contents_map)

    def test_get_fields_checkers_map(self):
        checkers_map = Task.get_fields_checkers_map()
        self.assertTrue(callable(checkers_map["name"]))
        self.assertTrue(callable(checkers_map["description"]))
        self.assertTrue(callable(checkers_map["deadline"]))
        self.assertTrue(callable(checkers_map["reminder"]))


    def test_contain_text(self):
        name = "Buy groceries"
        description = "Buy milk, bread, and eggs"
        task = Task(name, description, "2023-10-25 19:00", "2023-10-20 09:00")
        self.assertTrue(task.contain_text("groceries"))
        self.assertTrue(task.contain_text("eggs"))
        self.assertFalse(task.contain_text("cheese"))


    def test_to_string(self):
        name = "Buy groceries"
        description = "Buy milk, bread, and eggs"
        deadline = "2023-10-25 19:00"
        task = Task(name, description, deadline)
        expected_string = f"Name: {name}\nType: Task\nDescription: {description}\nDeadline: {deadline}\nReminder: "
        self.assertEqual(str(task), expected_string)

    def test_time_condition_checker(self):
        self.assertFalse(self.task.time_condition_checker(10.0, "<"))
        self.assertFalse(self.task.time_condition_checker(10.0, "="))
        self.assertTrue(self.task.time_condition_checker(10.0, ">"))

    def test_get_field_checker(self):
        name_checker = Task.get_field_checker("name")
        description_checker = Task.get_field_checker("description")
        deadline_checker = Task.get_field_checker("deadline")
        reminder_checker = Task.get_field_checker("reminder")
        self.assertTrue(callable(name_checker))
        self.assertTrue(callable(description_checker))
        self.assertTrue(callable(deadline_checker))
        self.assertTrue(callable(reminder_checker))

    def test_create_object_from_lines(self):
        lines = [
            "Name: Buy groceries",
            "Type: Task",
            "Description: Buy milk, bread, and eggs",
            "Deadline: 2023-10-25 19:00",
            "Reminder: None",
            "-------------------"
        ]
        index = 0
        expected_name = "Buy groceries"
        expected_description = "Buy milk, bread, and eggs"
        expected_deadline = "2023-10-25 19:00"
        expected_reminder = "None"
        task = Task.create_object_from_lines(lines, index)
        self.assertEqual(task.name, expected_name)
        self.assertEqual(task.description, expected_description)
        self.assertEqual(task.deadline, expected_deadline)
        self.assertEqual(task.reminder, expected_reminder)


if __name__ == "__main__":
    unittest.main()