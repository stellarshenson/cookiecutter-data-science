"""Test using ccds with our GitHub repo and --checkout master"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

GITHUB_REPO = "gh:stellarshenson/cookiecutter-data-science"
CHECKOUT_BRANCH = "master"


def _run_ccds(temp_dir: Path, project_name: str, env_manager: str, extra_args: dict = None):
    """Run ccds CLI with the GitHub repo."""
    args = [
        sys.executable, "-m", "cookiecutter",
        GITHUB_REPO,
        "--checkout", CHECKOUT_BRANCH,
        "--no-input",
        "--output-dir", str(temp_dir),
        f"project_name={project_name}",
        f"environment_manager={env_manager}",
        "python_version_number=3.12",
        "dependency_file=pyproject.toml",
        "jupyter_kernel_support=Yes",
    ]

    if extra_args:
        for key, value in extra_args.items():
            args.append(f"{key}={value}")

    result = subprocess.run(args, capture_output=True, text=True)
    return result


def _verify_project_structure(project_dir: Path, env_manager: str):
    """Verify basic project structure is correct."""
    # Core files that should always exist
    assert (project_dir / "Makefile").exists(), "Makefile should exist"
    assert (project_dir / "pyproject.toml").exists(), "pyproject.toml should exist"
    assert (project_dir / "README.md").exists(), "README.md should exist"
    assert (project_dir / ".gitignore").exists(), ".gitignore should exist"

    # Module directory with lib_ prefix
    module_dirs = [d for d in project_dir.iterdir() if d.is_dir() and d.name.startswith("lib_")]
    assert len(module_dirs) == 1, f"Expected one lib_* module directory, found {[d.name for d in module_dirs]}"
    module_dir = module_dirs[0]
    assert (module_dir / "__init__.py").exists(), "__init__.py should exist in module"

    # Conda should have environment.yml
    if env_manager == "conda":
        assert (project_dir / "environment.yml").exists(), "environment.yml should exist for conda"
    else:
        assert not (project_dir / "environment.yml").exists(), "environment.yml should not exist for non-conda"


def _verify_makefile_syntax(project_dir: Path):
    """Verify Makefile has valid syntax by running make help."""
    result = subprocess.run(
        ["make", "help"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"make help failed: {result.stderr}"
    assert "Available rules:" in result.stdout, "make help should list available rules"


@pytest.mark.skipif(
    os.environ.get("SKIP_GITHUB_TESTS", "0") == "1",
    reason="SKIP_GITHUB_TESTS is set"
)
class TestGitHubCheckout:
    """Test creating projects using ccds with GitHub repo checkout."""

    def test_conda_local(self):
        """Test conda project with local environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            result = _run_ccds(
                temp_path,
                "test_conda_gh",
                "conda",
                {"env_location": "local"}
            )

            assert result.returncode == 0, f"ccds failed: {result.stderr}"

            project_dir = temp_path / "test_conda_gh"
            assert project_dir.exists(), "Project directory should exist"

            _verify_project_structure(project_dir, "conda")
            _verify_makefile_syntax(project_dir)

    def test_uv(self):
        """Test uv project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            result = _run_ccds(temp_path, "test_uv_gh", "uv")

            assert result.returncode == 0, f"ccds failed: {result.stderr}"

            project_dir = temp_path / "test_uv_gh"
            assert project_dir.exists(), "Project directory should exist"

            _verify_project_structure(project_dir, "uv")
            _verify_makefile_syntax(project_dir)

    def test_virtualenv(self):
        """Test virtualenv project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            result = _run_ccds(temp_path, "test_venv_gh", "virtualenv")

            assert result.returncode == 0, f"ccds failed: {result.stderr}"

            project_dir = temp_path / "test_venv_gh"
            assert project_dir.exists(), "Project directory should exist"

            _verify_project_structure(project_dir, "virtualenv")
            _verify_makefile_syntax(project_dir)
