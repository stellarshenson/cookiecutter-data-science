"""
Tests for Copier template generation.

Mirrors test_creation.py but uses Copier instead of Cookiecutter.
Ensures the Copier template produces equivalent output to the Cookiecutter template.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from itertools import cycle, product
from pathlib import Path

import pytest
from env_matrix import get_absent_files, get_expected_files

CCDS_ROOT = Path(__file__).parents[1].resolve()
COPIER_DIR = CCDS_ROOT  # copier.yml is now at repo root


def is_copier_available():
    """Check if copier is installed."""
    try:
        result = subprocess.run(
            ["copier", "--version"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


# Skip all tests if copier is not installed
pytestmark = pytest.mark.skipif(
    not is_copier_available(),
    reason="copier not installed",
)


default_args = {
    "project_name": "my_test_project",
    "repo_name": "my-test-repo",
    "module_name": "lib_project_module",
    "author_name": "DrivenData",
    "description": "A test project",
}


def copier_config_generator(fast=False):
    """Generate test configurations for Copier tests.

    Mirrors the cookiecutter config_generator but uses Copier variable names.
    """
    ccds_json = json.load((CCDS_ROOT / "ccds.json").open("r"))

    # Python version - match the running version
    running_py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    py_version = [("python_version_number", v) for v in [running_py_version]]

    configs = product(
        py_version,
        [("environment_manager", opt) for opt in ccds_json["environment_manager"]],
        [("env_location", opt) for opt in ccds_json["env_location"]],
        [("dependency_file", opt) for opt in ccds_json["dependency_file"]],
        [("pydata_packages", opt) for opt in ccds_json["pydata_packages"]],
    )

    def _is_valid(config):
        config = dict(config)
        # env_location only applies to conda
        if (config["environment_manager"] != "conda") and (
            config["env_location"] == "global"
        ):
            return False
        # environment.yml only valid for conda
        if (config["environment_manager"] != "conda") and (
            config["dependency_file"] == "environment.yml"
        ):
            return False
        return True

    # Filter invalid configs
    configs = [c for c in configs if _is_valid(c)]

    # Cycle through linting and code scaffold options
    code_format_cycler = cycle(
        product(
            [
                ("include_code_scaffold", opt)
                for opt in ccds_json["include_code_scaffold"]
            ],
            [
                ("linting_and_formatting", opt)
                for opt in ccds_json["linting_and_formatting"]
            ],
        )
    )

    # Cycle through other options
    cycle_fields = [
        "open_source_license",
        "docs",
        "testing_framework",
        "jupyter_kernel_support",
    ]
    multi_select_cyclers = {k: cycle(ccds_json[k]) for k in cycle_fields}

    for ind, c in enumerate(configs):
        config = dict(c)
        config.update(default_args)

        code_format_settings = dict(next(code_format_cycler))
        config.update(code_format_settings)

        for field, cycler in multi_select_cyclers.items():
            config[field] = next(cycler)

        # Copier uses flat dataset_storage
        config["dataset_storage"] = "none"
        config["s3_bucket"] = ""
        config["s3_aws_profile"] = "default"
        config["azure_container"] = ""
        config["gcs_bucket"] = ""

        # Additional copier-specific defaults
        config["env_encryption"] = "No"  # Skip encryption for tests
        config["custom_config"] = ""

        config["repo_name"] += f"-copier-{ind}"
        config["env_name"] = config["repo_name"].replace("-", "_")

        yield config

        # Fast mode - single config
        if fast == 1 or fast >= 3:
            break


@contextmanager
def bake_copier_project(config):
    """Context manager to create a project with Copier and clean up after."""
    temp = Path(tempfile.mkdtemp(suffix="copier-project")).resolve()
    project_dir = temp / config["repo_name"]

    # Build copier command with data arguments
    cmd = [
        "copier",
        "copy",
        "--trust",
        "--defaults",
        str(COPIER_DIR),
        str(project_dir),
    ]

    # Add all config values as --data arguments
    for key, value in config.items():
        if key in ("repo_name",):
            continue  # Skip repo_name as it's the output dir
        # Convert Python bools/None to strings
        if isinstance(value, bool):
            value = str(value).lower()
        elif value is None:
            value = ""
        cmd.extend(["--data", f"{key}={value}"])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=temp,
    )

    if result.returncode != 0:
        print(f"Copier command failed:\n{' '.join(cmd)}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        raise RuntimeError(f"Copier failed with return code {result.returncode}")

    yield project_dir

    # Cleanup
    shutil.rmtree(temp)


def pytest_generate_tests(metafunc):
    """Generate test configurations for parametrized tests."""

    def make_test_id(config):
        env_loc = config.get("env_location", "local")
        return f"copier-{config['environment_manager']}-{env_loc}-{config['dependency_file']}-{config['pydata_packages']}"

    if "copier_config" in metafunc.fixturenames:
        metafunc.parametrize(
            "copier_config",
            copier_config_generator(metafunc.config.getoption("fast")),
            ids=make_test_id,
        )


def no_curlies(filepath):
    """Verify no unrendered Jinja templates in file."""
    data = filepath.open("r").read()
    template_strings = ["{{", "}}", "{%", "%}"]
    template_strings_in_file = [s in data for s in template_strings]
    return not any(template_strings_in_file)


def test_copier_baking_configs(copier_config, fast):
    """Test Copier project generation for various configurations."""
    print("using copier config", json.dumps(copier_config, indent=2))

    with bake_copier_project(copier_config) as project_directory:
        verify_copier_folders(project_directory, copier_config)
        verify_copier_files(project_directory, copier_config)


def verify_copier_folders(root, config):
    """Verify expected directories exist."""
    expected_dirs = [
        ".",
        "data",
        "data/external",
        "data/interim",
        "data/processed",
        "data/raw",
        "docs",
        "models",
        "notebooks",
        "references",
        "reports",
        "reports/figures",
        config["module_name"],
    ]

    if config["include_code_scaffold"] == "Yes":
        expected_dirs += [f"{config['module_name']}/modeling"]

    if config["docs"] == "mkdocs":
        expected_dirs += ["docs/docs"]

    if config.get("testing_framework", "pytest") != "none":
        expected_dirs += ["tests"]

    expected_dirs = [Path(d) for d in expected_dirs]

    # Exclude system directories
    excluded_dirs = {".ipynb_checkpoints", "__pycache__"}
    existing_dirs = [
        d.resolve().relative_to(root)
        for d in root.glob("**")
        if d.is_dir() and d.name not in excluded_dirs
    ]

    assert sorted(existing_dirs) == sorted(expected_dirs), (
        f"Directory mismatch for copier {config['environment_manager']} + {config['dependency_file']}\n"
        f"Missing: {set(expected_dirs) - set(existing_dirs)}\n"
        f"Extra: {set(existing_dirs) - set(expected_dirs)}"
    )


def verify_copier_files(root, config):
    """Verify expected files exist and no unexpected files present."""
    # Get expected files using the same matrix as cookiecutter
    expected_files = get_expected_files(config)

    # Copier adds .copier-answers.yml
    expected_files.append(".copier-answers.yml")

    expected_files = [Path(f) for f in expected_files]

    existing_files = [f.relative_to(root) for f in root.glob("**/*") if f.is_file()]

    assert sorted(existing_files) == sorted(set(expected_files)), (
        f"File mismatch for copier {config['environment_manager']} + {config['dependency_file']}\n"
        f"Missing: {set(expected_files) - set(existing_files)}\n"
        f"Extra: {set(existing_files) - set(expected_files)}"
    )

    # Verify files that should NOT exist
    absent_files = get_absent_files(config)
    for absent_file in absent_files:
        assert not (root / absent_file).exists(), (
            f"{absent_file} should not exist for copier "
            f"{config['environment_manager']} + {config['dependency_file']}"
        )

    # Verify no unrendered Jinja templates
    for f in existing_files:
        # Skip .copier-answers.yml as it contains template syntax documentation
        if f.name == ".copier-answers.yml":
            continue
        assert no_curlies(root / f), f"Unrendered Jinja template in {f}"


def test_copier_answers_file_created(fast):
    """Test that .copier-answers.yml is created with correct content."""
    config = next(copier_config_generator(fast=1))

    with bake_copier_project(config) as project_dir:
        answers_file = project_dir / ".copier-answers.yml"
        assert answers_file.exists(), ".copier-answers.yml should be created"

        content = answers_file.read_text()
        # Verify key configuration values are recorded
        # Note: project_name has when: false, so it's auto-derived and not in answers
        assert "repo_name" in content
        assert "environment_manager" in content
        assert "dependency_file" in content
