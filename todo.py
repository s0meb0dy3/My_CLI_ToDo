import os
import argparse
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.txt')
def add_task(task_description):
    """Add a new task to the list"""
    with open(TASKS_FILE, 'a') as f:
        f.write(task_description + '\n')
    print(f"Task added: {task_description}")

def list_tasks():
    """List all tasks from the tasks file"""
    if not os.path.exists(TASKS_FILE) or os.stat(TASKS_FILE).st_size == 0:
        print("No tasks found")
        return
    print("\n---Your To-Do List---")
    with open(TASKS_FILE, 'r') as f:
        for i,line in enumerate(f,1): 
            task=line.strip()
            print(f"{i}.{task}")
    print("---End of List---")

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

    # 'list' 命令
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # 解析命令行参数
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    else:
        parser.print_help() # 如果没有指定命令或命令无效，则打印帮助信息
    
if __name__ == "__main__":
    main()
