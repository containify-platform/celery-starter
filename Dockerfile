# One image for both apps: the web app runs the default command, the worker
# overrides it with `celery -A app.worker worker`.

# Build: install the locked dependencies into a virtualenv with uv.
FROM python:3.14-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Run: the virtualenv and the code, as a non-root user.
FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1 PATH="/app/.venv/bin:$PATH"
WORKDIR /app
RUN useradd --create-home --uid 1000 app
COPY --from=build /app/.venv /app/.venv
COPY app ./app
USER app
EXPOSE 8000
# [::]:8000 listens on IPv6 and IPv4.
CMD ["gunicorn", "app.web:app", "--bind", "[::]:8000", "--workers", "2", "--access-logfile", "-"]
