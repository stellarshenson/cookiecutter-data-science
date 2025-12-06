# Dockerfile for {{ cookiecutter.project_name }}
# Build: make docker_build
# Push: make docker_push

FROM python:{{ cookiecutter.python_version_number }}-slim

WORKDIR /app

# Copy and install the wheel (built by make build)
COPY dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl

# Copy entrypoint
COPY docker/entrypoint.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "entrypoint.py"]
