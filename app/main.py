from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from app.celery_app import celery
from app.tasks import example_task

app = FastAPI()

@app.post("/tasks")
def create_task(x: int, y: int):
    """Crear una nueva tarea y devolver su ID."""
    task = example_task.delay(x, y)
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """Obtener el estado de una tarea específica."""
    task_result = AsyncResult(task_id, app=celery)
    if not task_result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    """Eliminar una tarea de la cola (si es posible)."""
    task_result = AsyncResult(task_id, app=celery)
    if task_result.state == "PENDING":
        celery.control.revoke(task_id, terminate=True)
        return {"status": "Task revoked"}
    else:
        raise HTTPException(status_code=400, detail="Task cannot be revoked")

@app.get("/tasks")
def list_tasks():
    """Listar todas las tareas en curso o completadas."""
    # Este es un ejemplo, ya que Celery no almacena un historial completo por defecto.
    # Podrías implementar almacenamiento adicional en Redis o una BD para el historial.
    return {"detail": "Listing tasks is not natively supported in Celery without additional storage."}
