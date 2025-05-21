import os
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.txt')
def add_task(task_description):
    """Add a new task to the list"""
    with open(TASKS_FILE, 'a') as f:
        f.write(task_description + '\n')
    print(f"Task added: {task_description}")

def main():
    print("Welcom to MyCLI_ToDo!")
    add_task("Learn Linux")
    add_task("Learn Python")
    add_task("Learn Docker")
    add_task("Learn Kubernetes")
    add_task("Learn DevOps")
    add_task("Learn Cloud")
    
if __name__ == "__main__":
    main()
