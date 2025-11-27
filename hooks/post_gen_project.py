import shutil
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile

import tomlkit

# Attempt to import clone from cookiecutter, fall back to None if not available
try:
    from cookiecutter.vcs import clone as vcs_clone
except ImportError:
    vcs_clone = None


#
#  HELPER FUNCTIONS
#
def resolve_python_version_specifier(python_version):
    """Resolves the user-provided Python version string to a version specifier."""
    version_parts = python_version.split(".")
    if len(version_parts) == 2:
        major, minor = version_parts
        patch = "0"
        operator = "~="
    elif len(version_parts) == 3:
        major, minor, patch = version_parts
        operator = "=="
    else:
        raise ValueError(
            f"Invalid Python version specifier {python_version}. "
            "Please specify version as <major>.<minor> or <major>.<minor>.<patch>, "
            "e.g., 3.10, 3.10.1, etc."
        )

    resolved_python_version = ".".join((major, minor, patch))
    return f"{operator}{resolved_python_version}"


def write_python_version(python_version):
    with open("pyproject.toml", "r") as f:
        doc = tomlkit.parse(f.read())

    doc["project"]["requires-python"] = resolve_python_version_specifier(python_version)
    with open("pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(doc))


def write_custom_config(user_input_config):
    """Handle custom config overlay (inlined from ccds.hook_utils.custom_config)."""
    if not user_input_config:
        return

    tmp = TemporaryDirectory()
    tmp_zip = None

    print(user_input_config)

    # if not absolute, test if local path relative to parent of created directory
    if not user_input_config.startswith("/"):
        test_path = Path("..") / user_input_config
    else:
        test_path = Path(user_input_config)

    local_path = None

    # check if user passed a local path
    if test_path.exists() and test_path.is_dir():
        local_path = test_path

    elif test_path.exists() and str(test_path).endswith(".zip"):
        tmp_zip = test_path

    # check if user passed a url to a zip
    elif user_input_config.startswith("http") and (
        user_input_config.split(".")[-1] in ["zip"]
    ):
        tmp_zip, _ = urlretrieve(user_input_config)

    # assume it is a VCS uri and try to clone
    elif vcs_clone is not None:
        vcs_clone(user_input_config, clone_to_dir=tmp.name)
        local_path = Path(tmp.name)

    if tmp_zip:
        with ZipFile(tmp_zip, "r") as zipf:
            zipf.extractall(tmp.name)
            local_path = Path(tmp.name)

    # write whatever the user supplied into the project
    if local_path:
        copytree(local_path, ".", dirs_exist_ok=True)

    tmp.cleanup()


#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#

# {% if cookiecutter.linting_and_formatting == "ruff" %}
# ruff is in dev dependencies, not project dependencies
# Remove setup.cfg
Path("setup.cfg").unlink()
# {% elif cookiecutter.linting_and_formatting == "flake8+black+isort" %}
# flake8, black, isort are in dev dependencies, not project dependencies
# {% endif %}

# Select testing framework
tests_path = Path("tests")

# {% if cookiecutter.testing_framework == "pytest" %}
# pytest is in dev dependencies, not project dependencies
# {% endif %}

# ipykernel is installed during create_environment, not as a project dependency

# {% if cookiecutter.testing_framework == "none" %}
shutil.rmtree(tests_path)

# {% else %}
tests_subpath = tests_path / "{{ cookiecutter.testing_framework }}"
for obj in tests_subpath.iterdir():
    shutil.move(str(obj), str(tests_path))

# Remove all remaining tests templates
for tests_template in tests_path.iterdir():
    if tests_template.is_dir() and not tests_template.name == "tests":
        shutil.rmtree(tests_template)
# {% endif %}

# Use the selected documentation package specified in the config,
# or none if none selected
docs_path = Path("docs")
# {% if cookiecutter.docs != "none" %}
# docs package (mkdocs) is in dev dependencies, not project dependencies
docs_subpath = docs_path / "{{ cookiecutter.docs }}"
for obj in docs_subpath.iterdir():
    shutil.move(str(obj), str(docs_path))
# {% endif %}

# Remove all remaining docs templates
for docs_template in docs_path.iterdir():
    if docs_template.is_dir() and not docs_template.name == "docs":
        shutil.rmtree(docs_template)

#
#  POST-GENERATION FUNCTIONS
#
# For conda environments, keep environment.yml for dev dependencies (ipykernel, pytest, etc.)
# This keeps module dependencies in pyproject.toml clean
# For non-conda environments, delete environment.yml since it's not used
# {% if cookiecutter.environment_manager != "conda" %}
Path("environment.yml").unlink(missing_ok=True)
# {% endif %}

# Dependency file handling - see docs/docs/env-management.md for the full matrix
# - requirements.txt: keep requirements.txt and requirements-dev.txt, delete others
# - pyproject.toml: keep pyproject.toml (with dev deps), delete requirements files
# {% if cookiecutter.dependency_file == "pyproject.toml" %}
Path("requirements.txt").unlink(missing_ok=True)
Path("requirements-dev.txt").unlink(missing_ok=True)
# {% elif cookiecutter.dependency_file == "requirements.txt" and cookiecutter.environment_manager == "none" %}
# No environment manager means no dev dependencies needed
Path("requirements-dev.txt").unlink(missing_ok=True)
# {% endif %}

write_python_version("{{ cookiecutter.python_version_number }}")

write_custom_config("{{ cookiecutter.custom_config }}")

# Remove LICENSE if "No license file"
if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink()

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
pyproject_text = Path("pyproject.toml").read_text()
Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))

# {% if cookiecutter.include_code_scaffold == "No" %}
# remove everything except __init__.py so result is an empty package
for generated_path in Path("{{ cookiecutter.module_name }}").iterdir():
    if generated_path.is_dir():
        shutil.rmtree(generated_path)
    elif generated_path.name != "__init__.py":
        generated_path.unlink()
    elif generated_path.name == "__init__.py":
        # remove any content in __init__.py since it won't be available
        generated_path.write_text("")
# {% endif %}
