import unittest
from PIM.src.model.contact import Contact
from PIM.src.model.event import Event
from PIM.src.model.task import Task
from PIM.src.model.pim import PIM
from PIM.src.model.plain_text import PlainText

class PIMCreationTest(unittest.TestCase):
    def test_ContactCreationTest1(self):
        obj = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        self.assertIsInstance(obj,Contact)


    def test_ContactCreationTest2(self):
        obj = Contact.create("Jane Smith",{"mobile_number": "234-567-8901", "address": "456 Oak St."})
        self.assertIsInstance(obj,Contact)

    def test_ContactCreationTest3(self):
        obj = Task.create("Buy groceries", {"description": "Buy milk, bread, and eggs", "deadline": "2023-10-25 09:00"})
        self.assertNotIsInstance(obj,Contact)

    def test_TaskCreationTest1(self):
        obj = Task.create("Buy groceries", {"description": "Buy milk, bread, and eggs", "deadline": "2023-10-25 09:00"})
        self.assertIsInstance(obj,Task)

    def test_TaskCreationTest2(self):
        obj = Task.create("Attend meeting",
                                {"description": "Team sync-up", "deadline": "2023-10-21 09:00", "reminder": "2023-10-20 09:00"})
        self.assertIsInstance(obj,Task)

    def test_TaskCreationTest3(self):
        obj = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        self.assertNotIsInstance(obj, Task)


    def test_EventCreationTest1(self):
        obj = Event.create("Birthday party",
                                  {"description": "John's 30th birthday", "start_time": "2023-11-15 19:00",
                                   "alarms": ["2023-11-15 18:30"]})
        self.assertIsInstance(obj,Event)

    def test_EventCreationTest2(self):
        obj = Event.create("Concert", {"description": "Live music by The Beatles", "start_time": "2023-12-01 20:00",
                                              "alarms": ["2023-12-01 19:00", "2023-12-01 19:30"]})
        self.assertIsInstance(obj,Event)

    def test_EventCreationTest3(self):
        obj = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        self.assertNotIsInstance(obj, Event)

    def test_TextCreationTest1(self):
        obj = PlainText.create("Shopping List", {"text": "Milk, Bread, Eggs, Butter"})
        self.assertIsInstance(obj,PlainText)

    def test_TextCreationTest2(self):
        obj = PlainText.create("Poem", {"text": "Roses are red, Violets are blue."})
        self.assertIsInstance(obj,PlainText)

    def test_TestCreationTest3(self):
        obj = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        self.assertNotIsInstance(obj, PlainText)

    def test_PIMCreationTest1(self):
        obj = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        self.assertIsInstance(obj,PIM)

    def test_PIMCreationTest2(self):
        obj = PlainText.create("Shopping List", {"text": "Milk, Bread, Eggs, Butter"})
        self.assertIsInstance(obj, PIM)

    def test_PIMCreationTest3(self):
        obj = Task.create("Buy groceries", {"description": "Buy milk, bread, and eggs", "deadline": "2023-10-25 09:00"})
        self.assertIsInstance(obj, PIM)

    def test_PIMCreationTest4(self):
        obj = Contact.create("John Doe", {"mobile_number": "123-456-7890", "address": "123 Elm St."})
        self.assertIsInstance(obj, PIM)


if __name__ == '__main__':
    unittest.main()




