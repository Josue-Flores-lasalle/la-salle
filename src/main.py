from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos para las tareas
class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

# Base de datos simulada
tasks: List[Task] = []

# Rutas de la API
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Gestión de Tareas!"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    if any(existing_task.id == task.id for existing_task in tasks):
        raise HTTPException(status_code=400, detail="El ID ya existe")
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Tarea eliminada exitosamente"}
