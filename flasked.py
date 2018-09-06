import copy
import datetime
import json

from flask import Flask, redirect, render_template, request

from task import Task, TaskList


def load():
    try:
        tasklist = TaskList.from_json(json.load(open("todo.txt")))
    except FileNotFoundError:
        tasklist = TaskList.new()
    except json.decoder.JSONDecodeError:
        print("file has invalid data, starting from blank state")
        tasklist = TaskList.new()
    return tasklist


tasklist = load()

app = Flask(__name__)


def save():
    json.dump(tasklist.to_json(), open("todo.txt", "w"))


@app.route("/")
def index():
    return redirect("/tasks")


@app.route("/tasks")
def tasks():
    return render_template("tasks.html", tasks=tasklist.tasks)


@app.route("/tasks/<int:taskid>")
def task(taskid):
    return render_template("task.html", id=taskid, task=tasklist.tasks[taskid])


@app.route("/tasks/new", methods=["POST"])
def new_task():
    title = request.form["title"]
    tasklist.add(Task.new(title))
    save()
    return redirect("/tasks")


@app.route("/tasks/rename", methods=["POST"])
def rename_task():
    taskid = int(request.form["id"])
    title = request.form["title"]
    tasklist.rename(taskid, title)
    save()
    return redirect(f"/tasks/{taskid}")


@app.route("/tasks/delete", methods=["POST"])
def delete_task():
    taskid = int(request.form["id"])
    tasklist.delete(taskid)
    save()
    return redirect("/tasks")


@app.route("/tasks/reset", methods=["POST"])
def reset():
    global tasklist
    tasklist = TaskList.new()
    save()
    return redirect("/tasks")


@app.route("/tasks/reload", methods=["POST"])
def reload():
    global tasklist
    tasklist = load()
    save()
    return redirect("/tasks")
