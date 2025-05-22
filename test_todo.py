import unittest
import os
import tempfile
import shutil
from datetime import datetime, timedelta
import io
import sys

# Assuming todo.py is in the same directory or accessible in PYTHONPATH
import todo

class TestTodoApp(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to store tasks.txt
        self.test_dir = tempfile.mkdtemp()
        self.temp_tasks_file = os.path.join(self.test_dir, "temp_tasks.txt")
        
        # Patch todo.TASKS_FILE to use the temporary file
        self.original_tasks_file = todo.TASKS_FILE
        todo.TASKS_FILE = self.temp_tasks_file
        
        # Ensure the file is created for tests that might try to read/write it immediately
        with open(self.temp_tasks_file, 'w') as f:
            pass 

    def tearDown(self):
        # Restore original TASKS_FILE path
        todo.TASKS_FILE = self.original_tasks_file
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def _read_tasks_from_temp_file(self):
        if not os.path.exists(self.temp_tasks_file):
            return []
        with open(self.temp_tasks_file, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def _capture_stdout(self, func, *args, **kwargs):
        captured_output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            func(*args, **kwargs)
        finally:
            sys.stdout = old_stdout
        return captured_output.getvalue()

    # --- Test Cases for Task Deletion ---
    def test_delete_task_valid(self):
        todo.add_task("Task 1")
        todo.add_task("Task 2")
        todo.add_task("Task 3")
        
        todo.delete_task(2) # Delete "Task 2"
        
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 2)
        self.assertIn("Task 1", tasks)
        self.assertNotIn("Task 2", tasks)
        self.assertIn("Task 3", tasks)

    def test_delete_task_invalid_number_too_high(self):
        todo.add_task("Task 1")
        todo.add_task("Task 2")
        
        # Capture output to check for error message (optional, but good for CLI apps)
        output = self._capture_stdout(todo.delete_task, 3) 
        
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 2) # No task should be deleted
        self.assertIn("Invalid task number", output)

    def test_delete_task_invalid_number_zero(self):
        todo.add_task("Task 1")
        output = self._capture_stdout(todo.delete_task, 0)
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 1)
        self.assertIn("Invalid task number", output)

    def test_delete_task_non_numeric_input(self):
        todo.add_task("Task A")
        output = self._capture_stdout(todo.delete_task, "abc")
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 1) # No task should be deleted
        self.assertIn("Please enter a valid number", output)

    def test_delete_from_empty_list(self):
        # Ensure tasks file is empty (setUp does this)
        self.assertEqual(len(self._read_tasks_from_temp_file()), 0)
        
        output = self._capture_stdout(todo.delete_task, 1)
        
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 0) # Still empty
        self.assertIn("No tasks found", output) # Or similar message from your delete_task

    # --- Test Cases for Scheduled Tasks & Reminders ---
    def test_add_task_with_time(self):
        todo.add_task("Scheduled Task 1", "2023-12-25 10:30")
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], "Scheduled Task 1 || 2023-12-25 10:30")

    def test_add_task_without_time(self):
        todo.add_task("Simple Task")
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], "Simple Task")

    def test_list_tasks_display(self):
        todo.add_task("Task A (no time)")
        todo.add_task("Task B (future)", "2099-01-01 12:00")
        # Add a task that is past and reminded
        past_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        with open(self.temp_tasks_file, 'a') as f:
            f.write(f"Task C (past, reminded) || {past_time} || reminded\n")

        output = self._capture_stdout(todo.list_tasks)
        
        self.assertIn("1. Task A (no time)", output)
        self.assertIn(f"2. Task B (future) (Time: 2099-01-01 12:00)", output)
        self.assertIn(f"3. Task C (past, reminded) (Time: {past_time}) - Reminder Sent", output)

    def test_check_reminders_due_task(self):
        due_time_str = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
        todo.add_task("Due Task", due_time_str)
        
        output = self._capture_stdout(todo.check_reminders)
        
        self.assertIn(f"REMINDER: 'Due Task' was due on {due_time_str}", output)
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], f"Due Task || {due_time_str} || reminded")

    def test_check_reminders_future_task(self):
        future_time_str = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
        todo.add_task("Future Task", future_time_str)
        
        output = self._capture_stdout(todo.check_reminders)
        
        self.assertNotIn("REMINDER:", output)
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], f"Future Task || {future_time_str}") # Should not be marked reminded

    def test_check_reminders_already_reminded(self):
        past_time_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        task_line = f"Old Reminded Task || {past_time_str} || reminded"
        with open(self.temp_tasks_file, 'w') as f:
            f.write(task_line + '\n')
            
        output = self._capture_stdout(todo.check_reminders)
        
        self.assertNotIn("REMINDER:", output) # Should not print a new reminder
        tasks = self._read_tasks_from_temp_file()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], task_line) # State should be unchanged

    def test_check_reminders_mixed_tasks(self):
        past_due_str = (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
        future_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        already_reminded_past_str = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M")

        todo.add_task("Task 1 (Past Due)", past_due_str)
        todo.add_task("Task 2 (Future)", future_str)
        with open(self.temp_tasks_file, 'a') as f:
            f.write(f"Task 3 (Already Reminded) || {already_reminded_past_str} || reminded\n")
        todo.add_task("Task 4 (No Time)")
        
        output = self._capture_stdout(todo.check_reminders)
        
        self.assertIn(f"REMINDER: 'Task 1 (Past Due)' was due on {past_due_str}", output)
        self.assertNotIn("Task 2 (Future)", output) # Reminder for future task
        self.assertNotIn("Task 3 (Already Reminded)", output) # Reminder for already reminded
        self.assertNotIn("Task 4 (No Time)", output) # Reminder for no time task

        tasks = self._read_tasks_from_temp_file()
        expected_tasks = [
            f"Task 1 (Past Due) || {past_due_str} || reminded",
            f"Task 2 (Future) || {future_str}",
            f"Task 3 (Already Reminded) || {already_reminded_past_str} || reminded",
            "Task 4 (No Time)"
        ]
        # Reading from file might change order, so we check set equality or sort
        self.assertEqual(len(tasks), len(expected_tasks))
        self.assertCountEqual(tasks, expected_tasks) # Checks for same elements, regardless of order

if __name__ == '__main__':
    unittest.main()
