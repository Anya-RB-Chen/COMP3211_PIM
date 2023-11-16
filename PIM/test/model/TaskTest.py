import unittest
from PIM.src.model.Task import Task


class TaskTest(unittest.TestCase):
    def test1(self):
        obj = Task("Buy groceries", "Buy milk, bread, and eggs", "2023-10-25 09:00")
        self.assertIsInstance(obj, Task)
