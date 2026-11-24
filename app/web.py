from celery.result import AsyncResult
from flask import Flask, jsonify, request, url_for

from app.tasks import add
from app.worker import celery

app = Flask(__name__)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/")
def index():
    return {
        "message": "Hello from Flask and Celery on Containify",
        "try": "POST /tasks/add with {\"x\": 2, \"y\": 3}, then GET the URL it returns",
    }


@app.post("/tasks/add")
def enqueue_add():
    body = request.get_json(silent=True) or {}
    try:
        x, y = float(body.get("x", 0)), float(body.get("y", 0))
    except (TypeError, ValueError):
        return {"error": "x and y must be numbers"}, 400
    task = add.delay(x, y)
    return jsonify(id=task.id, url=url_for("task_status", task_id=task.id)), 202


@app.get("/tasks/<task_id>")
def task_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    body = {"id": task_id, "state": result.state}
    if result.successful():
        body["result"] = result.result
    elif result.failed():
        body["error"] = str(result.result)
    return body
