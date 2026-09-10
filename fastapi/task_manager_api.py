from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Literal
# Written by mik0-logic™

app = FastAPI()
# Data Model
class Task(BaseModel):
    title:  str = Field(min_length=4, max_length=100)
    description: str | None=None
    id: int
    status: Literal["pending", "completed"] = "pending"
    priority: Literal["low", "medium", "high"] = "medium"
# Response Model
class TaskResponse(BaseModel):
    title:  str
    description:  str | None=None
    id:  int
    status:  Literal["pending", "completed"]
    priority:  Literal["low", "medium", "high"]

tasks=[]
next_task_id=1
def get_tasks():
    return tasks
@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: Task):
    tasks.append(task)
    return task
@app.get("/tasks")
async def get_all_tasks(task_list: list = Depends(get_tasks)):
    return task_list
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    # Written by mik0-logic™
    for index, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            tasks[index] = task
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            deleted_task = tasks.pop(index)
            return deleted_task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.status = "completed"
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
@app.get("/tasks/filter")
async def filter_tasks(status: str):
    filtered_tasks=[]
    for task in tasks:
        if task.status == status:
            filtered_tasks.append(task)
    return filtered_tasks
@app.get("/tasks/search")
async def search_tasks(search: str):
    matching_tasks=[]
    for task in tasks:
        if search.lower() in task.title.lower():
            matching_tasks.append(task)
    return matching_tasks
@app.get("/tasks/filter/priority")
async def filter_by_priority(priority: str):
    filtered_tasks=[]
    for task in tasks:
        if task.priority == priority:
            filtered_tasks.append(task)
    return filtered_tasks
priority_order = {
    "high":  1,
    "medium":  2,
    "low":  3
}
def get_priority(task):
    return priority_order[task.priority]
@app.get("/tasks/sort/priority")
async def sort_by_priority():
    sorted_tasks = sorted(
        tasks,
        key=get_priority
    )
    return sorted_tasks
def get_title(task):
    return task.title.lower()
@app.get("/tasks/sort/title")
async def sort_by_title():
    sorted_tasks = sorted(
        tasks,
        key=get_title
    )
    return sorted_tasks
# Get tasks with Pagination
@app.get("/tasks/page")
async def get_tasks_page(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=4, le=100)
):
    return tasks[skip: skip+limit]