'''
Date: 2024-08-05 11:22:39
LastEditors: 牛智超
LastEditTime: 2024-08-06 14:21:15
FilePath: \tbScripte\commander\app\app.py
'''
import pika
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

from commander.app.api.v1.endpoints import users, items, auth

app = FastAPI()
app.include_router(users.router, prefix="/v1")
app.include_router(items.router, prefix="/v1")
app.include_router(auth.router, prefix="/v1")

# 注册 v2 版本的 API 路由
# app.include_router(v2_users.router, prefix="/v2")
# app.include_router(v2_items.router, prefix="/v2")
# app.include_router(v2_orders.router, prefix="/v2")
class Task(BaseModel):
    id: str
    description: str
    worker_limit: int
    workers: List[str] = []
    completed: bool = False

tasks = []

# RabbitMQ 连接设置
rabbitmq_host = '120.26.202.151'
rabbitmq_username ='nzc'
rabbitmq_password ='6116988.niu'
task_queue = 'task_queue'
result_queue = 'result_queue'

def publish_task(task):
    credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    connection_params = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=5672,
        virtual_host='/',
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=task_queue, arguments={'x-max-length': task.worker_limit})
    channel.basic_publish(exchange='',
                          routing_key=task_queue,
                          body=str(task))
    connection.close()

def publish_result(result):
    credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    connection_params = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=5672,
        virtual_host='/',
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=result_queue)
    channel.basic_publish(exchange='',
                          routing_key=result_queue,
                          body=str(result))
    connection.close()
    
@app.post("/tasks/", response_model=Task)
def create_task(description: str, worker_limit: int):
    task = Task(id=str(uuid.uuid4()), description=description, worker_limit=worker_limit)
    tasks.append(task)
    publish_task(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: str, worker_id: str):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    worker = next((worker for worker in task.workers if worker.worker_id == worker_id), None)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not assigned to this task")
    worker.status = "completed"
    worker.end_time = datetime.now()
    result = {"task_id": task_id, "worker_id": worker_id, "status": "completed", "end_time": worker.end_time.isoformat()}
    publish_result(result)
    return {"status": "Task completed"}
