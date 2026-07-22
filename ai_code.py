# Create a simple back-end CRUD API in FastAPI without a database where we can create task, read them, delete and update them, make the basic CRUD operation with proper error handling and basic pydantic data validation and return the apporiate status code at the success of the operation. 
# a in memory dictionary with the id, title and done boolean variable of the task
# Post request will assign the id number itself with a global count
# Make two endpoints
# 1) simple health checkpoint where you return status tell whether the API  is working or not
# 2) root endpoint which gives the description of the api in JSON format

# Additional endpoints will be
# 1. search based on a word like returning task with "milk" in them 
# 2. search based on id 
# 3. Stats total count and how many are tasks done or not


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI(
    title="Task CRUD API",
    description="A simple in-memory CRUD API using FastAPI",
    version="1.0.0"
)

# In-memory storage
tasks: Dict[int, dict] = {}
task_counter = 1


# -----------------------------
# Pydantic Models
# -----------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    done: bool | None = None


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to the Task CRUD API",
        "description": "Simple FastAPI CRUD API with in-memory storage.",
        "features": [
            "Create Task",
            "Read Tasks",
            "Update Task",
            "Delete Task",
            "Search by ID",
            "Search by Word",
            "Statistics"
        ]
    }


# -----------------------------
# Health Check Endpoint
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "API is working correctly"
    }


# -----------------------------
# Create Task
# -----------------------------

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global task_counter

    new_task = {
        "id": task_counter,
        "title": task.title,
        "done": task.done
    }

    tasks[task_counter] = new_task
    task_counter += 1

    return new_task


# -----------------------------
# Get All Tasks
# -----------------------------

@app.get("/tasks")
def get_all_tasks():
    return list(tasks.values())


# -----------------------------
# Search Task by ID
# -----------------------------

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return tasks[task_id]


# -----------------------------
# Update Task
# -----------------------------

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskUpdate):

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task = tasks[task_id]

    if updated.title is not None:
        task["title"] = updated.title

    if updated.done is not None:
        task["done"] = updated.done

    tasks[task_id] = task

    return task


# -----------------------------
# Delete Task
# -----------------------------

@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    deleted = tasks.pop(task_id)

    return {
        "message": "Task deleted successfully",
        "task": deleted
    }


# -----------------------------
# Search by Word
# -----------------------------

@app.get("/tasks/search/")
def search_tasks(word: str):

    result = [
        task
        for task in tasks.values()
        if word.lower() in task["title"].lower()
    ]

    return {
        "count": len(result),
        "tasks": result
    }


# -----------------------------
# Statistics
# -----------------------------

@app.get("/tasks/stats")
def task_stats():

    total = len(tasks)
    completed = sum(task["done"] for task in tasks.values())
    pending = total - completed

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }