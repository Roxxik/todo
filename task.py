import datetime


class Task:
    @staticmethod
    def from_json(json):
        return Task(
            title=json["title"],
            created_at=datetime.datetime.strptime(
                json["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
            ),
            updated_at=datetime.datetime.strptime(
                json["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"
            ),
        )

    def to_json(self):
        return {
            "title": self._title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def new(title):
        return Task(title, datetime.datetime.now(), datetime.datetime.now())

    def __init__(self, title, created_at, updated_at):
        self._title = title
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val
        self.updated_at = datetime.datetime.now()


class TaskList:
    @staticmethod
    def from_json(json):
        return TaskList(
            tasks={
                int(taskid): Task.from_json(task)
                for taskid, task in json["tasks"].items()
            },
            max_id=json["max_id"],
        )

    def to_json(self):
        return {
            "tasks": {taskid: task.to_json() for taskid, task in self.tasks.items()},
            "max_id": self._max_id,
        }

    @staticmethod
    def new():
        return TaskList(dict(), 0)

    def __init__(self, tasks, max_id):
        self.tasks = tasks
        self._max_id = max_id

    def add(self, task):
        self._max_id += 1
        self.tasks[self._max_id] = task
        return self._max_id

    def rename(self, taskid, title):
        self.tasks[taskid].title = title

    def delete(self, taskid):
        del self.tasks[taskid]
