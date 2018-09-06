import copy
import sys
import json

from task import TaskList, Task

try:
    tasklist = TaskList.from_json(json.load(open("todo.txt")))
except FileNotFoundError:
    tasklist = TaskList.new()
except json.decoder.JSONDecodeError:
    print("file has invalid data, starting from blank state")
    tasklist = TaskList.new()
if len(sys.argv) > 1 and sys.argv[1] == "list":
    for taskid, task in tasklist.tasks.items():
        print(f'{taskid}: "{task.to_json()}"')
elif len(sys.argv) > 2 and sys.argv[1] == "create":
    title = sys.argv[2]
    print(f'creating: "{title}"')
    taskid = tasklist.add(Task.new(title))
    print(f"created task {taskid}")
elif len(sys.argv) > 2 and sys.argv[1] == "delete":
    taskid = int(sys.argv[2])
    print(f'deleting: "{taskid}"')
    try:
        tasklist.delete(taskid)
    except ValueError:
        print(f'"{taskid}" not in list')
elif len(sys.argv) > 3 and sys.argv[1] == "rename":
    taskid = int(sys.argv[2])
    title = sys.argv[3]
    print(f'renaming: "{taskid}" to "{title}"')
    tasklist.rename(taskid, title)
else:
    print(f'unknown command: {" ".join(sys.argv)}')
    print("")
    print("usage:")
    print(f"{sys.argv[0]} create <name>")
    print(f"{sys.argv[0]} delete <task-id>")
    print(f"{sys.argv[0]} rename <task-id> <name>")
    print(f"{sys.argv[0]} list")
json.dump(tasklist.to_json(), open("todo.txt", "w"))
