import argparse
from task import create_task, Task, Priority, Status, modify_task, delete_task, search_tasks, sort_tasks, filter_tasks
from storage import load_tasks, save_tasks


def main():
    parser = argparse.ArgumentParser(description="Task Management CLI")
    parser.add_argument("action", choices=["add", "list", "modify", "delete", "search", "sort", "filter", "complete"])
    parser.add_argument("--title", help="Task title")
    parser.add_argument("--description", help="Task description")
    parser.add_argument("--due_date", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--priority", choices=["HIGH", "MEDIUM", "LOW"], help="Priority")
    parser.add_argument("--id", type=int, help="Task ID to modify or delete")
    parser.add_argument("--keyword", help="Keyword for search")
    parser.add_argument("--sort_by", choices=["due_date", "priority", "status"], help="Sort tasks by")
    parser.add_argument("--status", choices=["OPEN", "IN_PROGRESS", "COMPLETED"], help="Filter tasks by status")
    args = parser.parse_args()

    tasks = load_tasks()

    if args.action == "add":
        task = create_task(args.title, args.description, args.due_date, args.priority)
        tasks.append(task)
    elif args.action == "list":
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task}")
    elif args.action == "modify":
        if args.id:
            task_to_modify = tasks[args.id -1]
            kwargs = {}
            if args.title: kwargs['title'] = args.title
            if args.description: kwargs['description'] = args.description
            if args.due_date: kwargs['due_date'] = datetime.date.fromisoformat(args.due_date)
            if args.priority: kwargs['priority'] = Priority[args.priority.upper()]
            modify_task(task_to_modify, **kwargs)
    elif args.action == "delete":
        if args.id:
            delete_task(tasks, tasks[args.id - 1])
    elif args.action == "search":
        if args.keyword:
            results = search_tasks(tasks, args.keyword)
            for task in results:
                print(task)
    elif args.action == "sort":
        if args.sort_by:
            tasks = sort_tasks(tasks, args.sort_by)
            for task in tasks:
                print(task)
    elif args.action == "filter":
        if args.status:
            filtered_tasks = filter_tasks(tasks, status=Status[args.status])
            for task in filtered_tasks:
                print(task)
    elif args.action == "complete":
        if args.id:
            tasks[args.id - 1].mark_complete()

    save_tasks(tasks)


if __name__ == "__main__":
    main()

