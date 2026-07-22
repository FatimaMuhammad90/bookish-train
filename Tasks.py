
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
  title: str = Field(..., min_length=1)

class TaskUpdate(BaseModel):
  title: Optional[str] = Field(None, min_length=1)
  done: Optional[bool] = None

app = FastAPI()

tasks = {}
count = 0
@app.get("/")
def root():
    return { "name": "Task API",
             "version": "1.0",
             "endpoints": ["/tasks"] }

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/tasks")
def read():
    return tasks

@app.post("/tasks", status_code=201)
def create(task: TaskCreate):
    global count
    count += 1
    id = count
    title = task.title
    if id in tasks:
        raise HTTPException(status_code=409, detail="Task exists")
    tasks[id] = {"title": title, "done": False}
    return {"message": f"Added {title} to tasks."}
@app.get("/tasks/{id}")
def search(id: int):
    if id not in tasks:
         raise HTTPException(status_code=404, detail="Task not found")
    return tasks[id]


@app.put("/tasks/{id}")
def update(id: int, task: TaskUpdate):
    if id not in tasks:
         raise HTTPException(status_code=404, detail="Task not found")
    if task.title is None and task.done is None:
        raise HTTPException(status_code=400, detail="No fields to update")
    if task.title is not None:
        tasks[id]["title"] = task.title
    if task.done is not None:
        tasks[id]["done"] = task.done
    return {"message": f"Updated task with ID {id}."}


@app.delete("/tasks/{id}", status_code=204)
def delete(id: int):
    if id not in tasks:
         raise HTTPException(status_code=404, detail="Task not found")
    del tasks[id]
    return {}

