# Simple To-Do List Application

This is a command-line application for managing your to-do list. You can add tasks, list them, delete them, and even schedule tasks with reminders.

## Features

### Add a Task
You can add a new task to your to-do list.

**Syntax:**
```bash
python todo.py add "Your task description here"
```

**Scheduled Tasks:**
You can also add a task with a specific due date and time.

**Syntax:**
```bash
python todo.py add "Your scheduled task description" --time "YYYY-MM-DD HH:MM"
```
*   `YYYY-MM-DD HH:MM`: Specify the year, month, day, hour, and minute for the task. For example, "2023-12-25 10:30".

### List Tasks
View all your current tasks. Tasks with a scheduled time will display the time. If a reminder has been sent for a scheduled task, it will be indicated.

**Syntax:**
```bash
python todo.py list
```
The output will number each task, which is used for deleting tasks.

### Delete a Task
Remove a task from your list using its number (obtained from the `list` command).

**Syntax:**
```bash
python todo.py delete <task_number>
```
*   `<task_number>`: The number of the task you want to delete, as shown in the `list` command output.

### Check Reminders
Check for any scheduled tasks that are past their due time.

**Syntax:**
```bash
python todo.py remind
```
*   If a scheduled task is due (its time is in the past), a reminder message will be printed.
*   Once a reminder has been shown for a task, it will be marked as "reminded" to prevent repeated notifications for the same task. The `list` command will show "(Time: YYYY-MM-DD HH:MM) - Reminder Sent" for such tasks.

## Getting Started

1.  Ensure you have Python installed.
2.  Save the script as `todo.py`.
3.  Run the script from your terminal using the commands described above.
    For example: `python todo.py add "Buy groceries"`

## Task Storage
Tasks are stored in a file named `tasks.txt` in the same directory as the `todo.py` script.
If tasks have a scheduled time, they are stored in the format:
`task_description || YYYY-MM-DD HH:MM`
If a reminder has been sent, it's stored as:
`task_description || YYYY-MM-DD HH:MM || reminded`