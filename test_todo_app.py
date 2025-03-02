import unittest
from todo_app import TodoList
import os
import json

class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.todo = TodoList()
        # Ensure we're using a test JSON file
        self.todo.tasks = []
        
    def tearDown(self):
        # Clean up any test files
        if os.path.exists('tasks.json'):
            os.remove('tasks.json')

    def test_add_task(self):
        task = self.todo.add_task("Test task")
        self.assertEqual(task['description'], "Test task")
        self.assertEqual(task['completed'], False)
        self.assertEqual(len(self.todo.tasks), 1)

    def test_complete_task(self):
        task = self.todo.add_task("Test task")
        result = self.todo.complete_task(task['id'])
        self.assertTrue(result)
        self.assertTrue(self.todo.tasks[0]['completed'])

    def test_delete_task(self):
        task = self.todo.add_task("Test task")
        initial_length = len(self.todo.tasks)
        result = self.todo.delete_task(task['id'])
        self.assertTrue(result)
        self.assertEqual(len(self.todo.tasks), initial_length - 1)

    def test_save_and_load_tasks(self):
        self.todo.add_task("Test task")
        self.todo.save_tasks()
        
        # Create new instance to test loading
        new_todo = TodoList()
        self.assertEqual(len(new_todo.tasks), 1)
        self.assertEqual(new_todo.tasks[0]['description'], "Test task")

if __name__ == '__main__':
    unittest.main()