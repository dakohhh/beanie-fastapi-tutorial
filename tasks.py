from fastapi import APIRouter, HTTPException, status
from models import Task, TaskCreate, TaskUpdate
from typing import List
from beanie import PydanticObjectId

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
async def get_all_task() -> List[Task]:

    tasks = await Task.find_all().to_list()

    return tasks


@router.post("/")
async def create_task(task: TaskCreate):

    task = await Task(**task.model_dump()).save()

    # print(task)

    return task



@router.get("/{task_id}")
async def get_task(task_id: PydanticObjectId):

    task = await Task.get(task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={ "message": "Task not Found" })

    return task


@router.put("/{task_id}")
async def update_task(task_id: PydanticObjectId, task_update: TaskUpdate):

    task = await Task.get(task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Task not Found"})
    
    # Update the fields on the task instance
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    # Use replace to trigger the before_event of the updated_at (beanie bug)
    updated_task = await task.replace()

    return updated_task



@router.delete("/{task_id}")
async def delete_task(task_id: PydanticObjectId):

    task = await Task.get(task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Task not Found"})
    

    await task.delete()

    return {"message": "Task deleted successfully"}