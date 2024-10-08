from fastapi import FastAPI, Depends
from app.database import tasks_collection
from app.models import Task
from app.rabbitmq import publish_message


app = FastAPI()


@app.post("/tasks/")
async def create_task(task: Task):
    task_data = task.dict()
    tasks_collection.insert_one(task_data)
    
    publish_message(f"Task '{task.title}' assigned to {task.assigned_to}")
    
    return {"message": "Task created successfully"}
