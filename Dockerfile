FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove build-essential

RUN pip install uv 
    
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml .

RUN uv sync

FROM python:3.11-slim-bookworm AS production 

RUN pip install uv

WORKDIR /app

COPY . .
COPY --from=builder /app/.venv .venv

ENV PATH="/root/.local/bin:$PATH:/app/.venv/bin"
ENV PYTHONPATH="/app/.venv/lib/python3.11/site-packages:$PYTHONPATH"

CMD ["uv", "run", "sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
