# Install the locked Python dependencies into the image.
FROM ghcr.io/astral-sh/uv:0.9.9 AS uv
FROM python:3.13-slim AS runtime

COPY --from=uv /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# The test image adds pytest and httpx; runtime stays small and excludes dev tools.
FROM runtime AS test
RUN uv sync --frozen

# Keep the default image target on the minimal runtime stage.
FROM runtime AS production
