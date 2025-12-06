"""Docker integration tests for the cookiecutter template.

These tests verify that:
- make docker_build creates a valid Docker image
- make docker_run executes successfully

Tests are skipped if Docker is not available or not running.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import bake_project

# Check if Docker is available
DOCKER_AVAILABLE = shutil.which("docker") is not None


def docker_is_running():
    """Check if Docker daemon is running."""
    if not DOCKER_AVAILABLE:
        return False
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False


DOCKER_RUNNING = docker_is_running()

# Skip all tests in this module if Docker is not available or not running
pytestmark = pytest.mark.skipif(
    not DOCKER_RUNNING,
    reason="Docker is not available or not running",
)


# Test configuration with docker_support enabled
DOCKER_CONFIG = {
    "project_name": "docker_test_project",
    "repo_name": "docker_test_project",
    "module_name": "lib_docker_test_project",
    "author_name": "Test Author",
    "description": "Test project for Docker",
    "open_source_license": "MIT",
    "python_version_number": "3.12",
    "environment_manager": "uv",
    "dependency_file": "requirements.txt",
    "include_code_scaffold": "Yes",
    "docs": "none",
    "testing_framework": "pytest",
    "linting_and_formatting": "ruff",
    "docker_support": "Yes",
    "env_encryption": "No",
}


class TestDockerWorkflow:
    """Test Docker build and run workflow."""

    def test_docker_build_and_run(self):
        """Test that make docker_run succeeds (which runs docker_build first)."""
        with bake_project(DOCKER_CONFIG) as project_directory:
            # Verify docker files exist
            dockerfile = project_directory / "docker" / "Dockerfile"
            entrypoint = project_directory / "docker" / "entrypoint.py"
            assert dockerfile.exists(), "Dockerfile should exist"
            assert entrypoint.exists(), "entrypoint.py should exist"

            # Run make docker_run (which depends on docker_build -> build)
            result = subprocess.run(
                ["make", "docker_run"],
                cwd=project_directory,
                capture_output=True,
                timeout=300,  # 5 minute timeout for build
            )

            stdout = result.stdout.decode("utf-8")
            stderr = result.stderr.decode("utf-8")

            print("\n======================= STDOUT ======================")
            print(stdout)
            print("\n======================= STDERR ======================")
            print(stderr)

            assert result.returncode == 0, (
                f"make docker_run failed with code {result.returncode}\n"
                f"stdout: {stdout}\n"
                f"stderr: {stderr}"
            )

            # Verify the container ran and printed version info
            assert "Running docker_test_project" in stdout or "Running docker_test_project" in stderr

    def test_docker_files_not_present_when_disabled(self):
        """Test that docker files are not created when docker_support is No."""
        config_no_docker = DOCKER_CONFIG.copy()
        config_no_docker["docker_support"] = "No"

        with bake_project(config_no_docker) as project_directory:
            docker_dir = project_directory / "docker"
            assert not docker_dir.exists(), "docker/ directory should not exist when docker_support=No"
