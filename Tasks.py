import datetime

from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    name: str
    date: datetime  
app = FastAPI()

tasks = {}


@app.post("/")
def create(task: Task):
    name = task.name
    if name in tasks:
        raise HTTPException(status_code=409, detail="Task exists")
    tasks[name] = task
    return {"message": f"Added {name} to tasks."}
 