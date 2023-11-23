import unittest
import sys
sys.path.append("..")
from PIM.src.model.event import Event


class EventTests(unittest.TestCase):
    def setUp(self):
        self.event = Event("Meeting", "Team meeting", "2022-01-01 09:00", "2022-01-01 08:45")

    def test_create(self):
        fields_map = {
            "description": "Project kick-off",
            "start_time": "2022-02-01 10:00",
            "alarms": "09:30"
        }
        event = Event.create("Meeting", fields_map)
        self.assertEqual(event.name, "Meeting")
        self.assertEqual(event.description, "Project kick-off")
        self.assertEqual(event.start_time, "2022-02-01 10:00")
        self.assertEqual(event.alarms, "09:30")

    def test_get_fields(self):
        fields = Event.get_fields()
        expected_fields = ["name", "description", "start_time", "alarms"]
        self.assertEqual(fields, expected_fields)

    def test_get_explanation(self):
        explanation = Event.get_explanation()
        expected_explanation = "An event is an occurrence that happens at a specific time and place, with a description and optional alarms."
        self.assertEqual(explanation, expected_explanation)

    def test_get_fields_contents_map(self):
        contents_map = self.event.get_fields_contents_map()
        expected_map = {
            "name": "Meeting",
            "description": "Team meeting",
            "start_time": "2022-01-01 09:00",
            "alarms": "2022-01-01 08:45"
        }
        self.assertEqual(contents_map, expected_map)

    def test_get_fields_checkers_map(self):
        checkers_map = Event.get_fields_checkers_map()
        self.assertTrue(callable(checkers_map["name"]))
        self.assertTrue(callable(checkers_map["description"]))
        self.assertTrue(callable(checkers_map["start_time"]))
        self.assertTrue(callable(checkers_map["alarms"]))

    def test_contain_text(self):
        self.assertTrue(self.event.contain_text("Meeting"))
        self.assertTrue(self.event.contain_text("Team"))
        self.assertFalse(self.event.contain_text("Project"))

    def test_str(self):
        expected_str = "Name: Meeting\nType: Event\nDescription: Team meeting\nStart time: 2022-01-01 09:00\nAlarms: " \
                       "2022-01-01 08:45"
        self.assertEqual(str(self.event), expected_str)

    def test_time_condition_checker(self):
        # Test with start_time
        self.assertFalse(self.event.time_condition_checker(1641066000.0, ">"))
        self.assertTrue(self.event.time_condition_checker(1641066000.0, "<"))
        self.assertFalse(self.event.time_condition_checker(1641066000.0, "="))

        # Test with alarms
        self.assertFalse(self.event.time_condition_checker(1641065700.0, ">"))
        self.assertTrue(self.event.time_condition_checker(1641065700.0, "<"))
        self.assertFalse(self.event.time_condition_checker(1641065700.0, "="))

        # Test with invalid comparator
        self.assertFalse(self.event.time_condition_checker(1641066000.0, "invalid"))

    def test_get_field_checker(self):
        name_checker = Event.get_field_checker("name")
        self.assertTrue(callable(name_checker))

    def test_create_object_from_lines(self):
        lines = [
            "Name: Meeting\n",
            "Type: Event\n",
            "Description: Team meeting\n",
            "Start time: 2022-01-01 09:00\n",
            "Alarms: 2022-01-01 08:45\n"
        ]
        index = 0
        event = Event.create_object_from_lines(lines, index)
        self.assertEqual(event.name, "Meeting")
        self.assertEqual(event.description, "Team meeting")
        self.assertEqual(event.start_time, "2022-01-01 09:00")
        self.assertEqual(event.alarms, "2022-01-01 08:45")


if __name__ == "__main__":
    unittest.main()
