FROM python:3.12-slim

# disable buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
# uv settings
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_SYNC=1

WORKDIR /srv/inventory_management_exercise

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY README.md pyproject.toml uv.lock ./

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy application code
COPY ./src/inventory_management_exercise ./src/inventory_management_exercise

ENV UVICORN_PORT=8080
EXPOSE $UVICORN_PORT

# Example startup command for uvicorn webserver for use in deployment manifest
# CMD ["uv", "run", "uvicorn", "inventory_management_exercise.main:app", "--host", "0.0.0.0"]
