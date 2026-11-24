# Celery starter

A [Flask](https://flask.palletsprojects.com/) web app and a [Celery](https://docs.celeryq.dev/)
worker that share a Valkey (Redis-compatible) broker, ready to deploy on
[Containify](https://containify.net). Both run from the same image with different commands.

- `GET /`: a hello message
- `POST /tasks/add` (`{"x": 2, "y": 3}`): queues a task and returns its id and status URL
- `GET /tasks/<id>`: the task's state and, once the worker has run it, its result
- `GET /health`: the health check

| App | Command |
| --- | --- |
| Web | `gunicorn app.web:app --bind [::]:8000` (the image's default) |
| Worker | `celery -A app.worker worker --loglevel INFO --concurrency 2` |

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` and `uv.lock`).

## Run it locally

```bash
docker run -d --name valkey -p 6379:6379 valkey/valkey:9-alpine
export REDIS_URL=redis://localhost:6379/0
uv sync
uv run celery -A app.worker worker --loglevel INFO &
uv run flask --app app.web run
curl -X POST localhost:5000/tasks/add -H 'content-type: application/json' -d '{"x": 2, "y": 3}'
```

## Deploy on Containify

Deploy the **Celery starter** template from the Containify catalogue. It adds the web app, the
worker and a private Valkey, and gives both apps `REDIS_URL`. Only the web app is public.
Add tasks in `app/tasks.py`; to run more of them at once, raise the worker's replicas or its
`--concurrency`.

## License

MIT
