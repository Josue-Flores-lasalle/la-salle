from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "¡Bienvenido a la API de Gestión de Tareas!"}

def test_create_task():
    task = {"id": 1, "title": "Comprar comida", "description": "Ir al supermercado", "completed": False}
    response = client.post("/tasks", json=task)
    assert response.status_code == 200
    assert response.json() == task

def test_get_task():
    task_id = 1
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task():
    updated_task = {"id": 1, "title": "Comprar comida", "description": "Ir al mercado local", "completed": True}
    response = client.put("/tasks/1", json=updated_task)
    assert response.status_code == 200
    assert response.json() == updated_task

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Tarea eliminada exitosamente"}

def test_task_not_found():
    response = client.get("/tasks/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarea no encontrada"}