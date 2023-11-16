import unittest
from PIM.src.model.Contact import Contact
from PIM.src.model.Event import Event

class ContactTest(unittest.TestCase):
    def is_instance_test(self):
        obj = Contact("John Doe","123-456-7890","123 Elm St.")
        self.assertIsInstance(obj,Contact)


    def not_instance_test(self):
        obj = Contact("Mike", "666-666-6666", "456 Elm St.")
        self.assertNotIsInstance(obj,Event)





