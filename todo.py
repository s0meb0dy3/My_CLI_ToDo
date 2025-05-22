import os
import argparse
from datetime import datetime
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.txt')
def add_task(task_description, task_time=None):
    """Add a new task to the list"""
    with open(TASKS_FILE, 'a') as f:
        if task_time:
            f.write(f"{task_description} || {task_time}\n")
            print(f"Task added: {task_description} at {task_time}")
        else:
            f.write(task_description + '\n')
            print(f"Task added: {task_description}")

def list_tasks():
    """List all tasks from the tasks file"""
    if not os.path.exists(TASKS_FILE) or os.stat(TASKS_FILE).st_size == 0:
        print("No tasks found")
        return
    print("\n---Your To-Do List---")
    with open(TASKS_FILE, 'r') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            parts = line.split(" || ")
            task_description = parts[0]
            if len(parts) >= 2: # Has time
                task_time = parts[1]
                # Check if it's marked as reminded (parts[2] would be "reminded")
                # We don't want to show "reminded" or the raw time string if it was just a description before
                if task_time == "reminded" and len(parts) == 2: # Should not happen with current add_task logic
                     print(f"{i}. {task_description}")
                elif len(parts) > 2 and parts[2] == "reminded":
                     print(f"{i}. {task_description} (Time: {task_time}) - Reminder Sent")
                else: # Has time, not reminded
                     print(f"{i}. {task_description} (Time: {task_time})")
            else: # No time
                print(f"{i}. {task_description}")
    print("---End of List---")

def check_reminders():
    """Check for tasks that are due and print reminders."""
    if not os.path.exists(TASKS_FILE) or os.stat(TASKS_FILE).st_size == 0:
        print("No tasks to check for reminders.")
        return

    now = datetime.now()
    updated_tasks = []
    reminders_found = False

    with open(TASKS_FILE, 'r') as f:
        tasks = f.readlines()

    for task_line in tasks:
        task_line_stripped = task_line.strip()
        parts = task_line_stripped.split(" || ")
        
        if len(parts) >= 2: # Task has a time
            description = parts[0]
            task_time_str = parts[1]
            is_reminded = len(parts) > 2 and parts[2] == "reminded"

            if not is_reminded:
                try:
                    task_time = datetime.strptime(task_time_str, "%Y-%m-%d %H:%M")
                    if task_time <= now:
                        print(f"REMINDER: '{description}' was due on {task_time_str}")
                        updated_tasks.append(f"{description} || {task_time_str} || reminded\n")
                        reminders_found = True
                    else:
                        updated_tasks.append(task_line) # Task is not due yet
                except ValueError:
                    # Malformed time string, keep original task line
                    updated_tasks.append(task_line)
            else:
                updated_tasks.append(task_line) # Already reminded
        else:
            updated_tasks.append(task_line) # Task does not have a time

    if reminders_found:
        with open(TASKS_FILE, 'w') as f:
            f.writelines(updated_tasks)
    elif not any(" || " in task for task in tasks if "reminded" not in task.split(" || ")[-1]):
        print("No pending tasks with due times found.")
    else:
        print("No tasks are currently due.")


def delete_task(task_number):
    """Delete a task from the list"""
    if not os.path.exists(TASKS_FILE):
        print("No tasks found")
        return
        
    with open(TASKS_FILE, 'r') as f:
        tasks = f.readlines()
        
    if not tasks:
        print("No tasks found")
        return
        
    try:
        task_number = int(task_number)
        if task_number < 1 or task_number > len(tasks):
            print(f"Invalid task number. Please enter a number between 1 and {len(tasks)}")
            return
            
        deleted_task = tasks.pop(task_number - 1)
        
        with open(TASKS_FILE, 'w') as f:
            f.writelines(tasks)
            
        print(f"Task deleted: {deleted_task.strip()}")
        
    except ValueError:
        print("Please enter a valid number")
        
def main():
    parser = argparse.ArgumentParser(description="A simple command-line To-Do application.")

    # 定义子命令
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'add' 命令
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="The description of the task")
    add_parser.add_argument("--time", type=str, help="Optional time for the task in YYYY-MM-DD HH:MM format")

    # 'list' 命令
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # 'delete' 命令
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_number", type=int, help="The number of the task to delete")

    # 'remind' 命令
    remind_parser = subparsers.add_parser("remind", help="Check for task reminders")

    # 解析命令行参数
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description, args.time)
    elif args.command == "list":
        list_tasks()
    elif args.command == "delete":
        delete_task(args.task_number)
    elif args.command == "remind":
        check_reminders()
    else:
        parser.print_help() # 如果没有指定命令或命令无效，则打印帮助信息
    
if __name__ == "__main__":
    main()
