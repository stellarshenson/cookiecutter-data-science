# Dockerfile for {{ cookiecutter.project_name }}
# Build: make docker_build
# Push: make docker_push

FROM python:{{ cookiecutter.python_version_number }}-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better caching
{% if cookiecutter.dependency_file == 'requirements.txt' -%}
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
{% elif cookiecutter.dependency_file == 'pyproject.toml' -%}
COPY pyproject.toml .
RUN pip install --no-cache-dir .
{% endif %}

# Copy application code
COPY {{ cookiecutter.module_name }}/ ./{{ cookiecutter.module_name }}/
COPY docker/entrypoint.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "entrypoint.py"]
