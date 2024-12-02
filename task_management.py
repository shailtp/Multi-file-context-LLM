# Task Management System

# A dictionary to store tasks
tasks = {}

def add_task(task_id, title, description, priority):
    """Adds a task to the system."""
    if task_id in tasks:
        print(f"Task ID {task_id} already exists.")
        return
    tasks[task_id] = {
        'title': title,
        'description': description,
        'priority': priority,
        'status': 'Pending'
    }
    print(f"Task '{title}' added successfully.")

def delete_task(task_id):
    """Deletes a task from the system."""
    if task_id in tasks:
        del tasks[task_id]
        print(f"Task ID {task_id} deleted successfully.")
    else:
        print(f"Task ID {task_id} not found.")

def mark_task_completed(task_id):
    """Marks a task as completed."""
    if task_id in tasks:
        tasks[task_id]['status'] = 'Completed'
        print(f"Task ID {task_id} marked as completed.")
    else:
        print(f"Task ID {task_id} not found.")

def get_task(task_id):
    """Fetches the details of a specific task."""
    return tasks.get(task_id, f"Task ID {task_id} not found.")

def list_tasks():
    """Lists all tasks in the system."""
    if not tasks:
        print("No tasks available.")
        return
    for task_id, task_details in tasks.items():
        print(f"ID: {task_id} | Title: {task_details['title']} | Status: {task_details['status']}")

def filter_tasks_by_status(status):
    """Filters tasks by their status."""
    return {tid: t for tid, t in tasks.items() if t['status'] == status}

def list_pending_tasks():
    """Lists all pending tasks."""
    pending_tasks = filter_tasks_by_status('Pending')
    if not pending_tasks:
        print("No pending tasks.")
        return
    print("Pending Tasks:")
    for task_id, task in pending_tasks.items():
        print(f"ID: {task_id} | Title: {task['title']}")

def list_completed_tasks():
    """Lists all completed tasks."""
    completed_tasks = filter_tasks_by_status('Completed')
    if not completed_tasks:
        print("No completed tasks.")
        return
    print("Completed Tasks:")
    for task_id, task in completed_tasks.items():
        print(f"ID: {task_id} | Title: {task['title']}")

def update_task_priority(task_id, new_priority):
    """Updates the priority of a task."""
    if task_id in tasks:
        tasks[task_id]['priority'] = new_priority
        print(f"Task ID {task_id} priority updated to {new_priority}.")
    else:
        print(f"Task ID {task_id} not found.")

def auto_prioritize():
    """Automatically updates priorities based on some logic."""
    for task_id, task in tasks.items():
        if task['status'] == 'Pending' and task['priority'] < 5:
            update_task_priority(task_id, task['priority'] + 1)

def archive_completed_tasks():
    """Archives and removes completed tasks."""
    completed_tasks = filter_tasks_by_status('Completed')
    for task_id in completed_tasks.keys():
        delete_task(task_id)

def task_summary():
    """Prints a summary of tasks."""
    total_tasks = len(tasks)
    completed_tasks = len(filter_tasks_by_status('Completed'))
    pending_tasks = total_tasks - completed_tasks
    print("Task Summary:")
    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Pending Tasks: {pending_tasks}")

def main():
    """Main function to demonstrate functionality."""
    # Adding tasks
    add_task(1, "Complete Python Code", "Write a Python script with >10 functions", 3)
    add_task(2, "Review PR", "Review the pull request in GitHub", 4)
    add_task(3, "Workout", "Complete 30-minute HIIT session", 2)

    # Listing tasks
    print("\nAll Tasks:")
    list_tasks()

    # Updating priorities and marking tasks
    print("\nUpdating priorities and marking task completed:")
    update_task_priority(1, 5)
    mark_task_completed(1)

    # Filtering and listing tasks
    print("\nPending Tasks:")
    list_pending_tasks()
    print("\nCompleted Tasks:")
    list_completed_tasks()

    # Auto-prioritizing tasks
    print("\nAuto-prioritizing tasks:")
    auto_prioritize()
    list_tasks()

    # Archiving completed tasks
    print("\nArchiving completed tasks:")
    archive_completed_tasks()
    list_tasks()

    # Task summary
    print("\nTask Summary:")
    task_summary()

# Entry point
if __name__ == "__main__":
    main()
