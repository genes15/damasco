from celery import Celery
import os

# Configuración de Celery con Redis como backend y broker
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery = Celery("app.tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.update(task_track_started=True)

# Importa las tareas
#celery.config_from_object("celeryconfig")
celery.autodiscover_tasks(['app.tasks'])