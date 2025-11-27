import shutil
from copy import copy
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
#  PACKAGE LISTS (inlined from ccds.hook_utils.dependencies)
#
packages = [
    "python-dotenv",
]

flake8_black_isort = [
    "black",
    "flake8",
    "isort",
]

ruff = ["ruff"]

basic = [
    "matplotlib",
    "numpy",
    "pandas",
    "scikit-learn",
]

scaffold = [
    "typer",
    "loguru",
    "tqdm",
]


#
#  HELPER FUNCTIONS (inlined from ccds.hook_utils.dependencies)
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


def write_dependencies(
    dependencies,
    packages,
    pip_only_packages,
    repo_name,
    module_name,
    python_version,
    environment_manager=None,
    description=None,
):
    if dependencies == "requirements.txt":
        with open(dependencies, "w") as f:
            lines = sorted(packages)

            lines += ["" "-e ."]

            f.write("\n".join(lines))
            f.write("\n")

    elif dependencies == "pyproject.toml":
        with open(dependencies, "r") as f:
            doc = tomlkit.parse(f.read())

        # Standard pyproject.toml dependencies
        # Check if dependencies already exists (e.g., from template with code scaffold)
        if "dependencies" in doc["project"]:
            # Merge with existing dependencies
            existing_deps = list(doc["project"]["dependencies"])
            all_deps = sorted(set(existing_deps + packages))
            doc["project"]["dependencies"].clear()
            for dep in all_deps:
                doc["project"]["dependencies"].append(dep)
        else:
            doc["project"].add("dependencies", sorted(packages))
        doc["project"]["dependencies"].multiline(True)

        with open(dependencies, "w") as f:
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
packages_to_install = copy(packages)

# {% if cookiecutter.dataset_storage.s3 %}
packages_to_install += ["awscli"]
# {% endif %} #

# {% if cookiecutter.include_code_scaffold == "Yes" %}
packages_to_install += scaffold
# {% endif %}

# {% if cookiecutter.pydata_packages == "basic" %}
packages_to_install += basic
# {% endif %}

# {% if cookiecutter.linting_and_formatting == "ruff" %}
packages_to_install += ruff
# Remove setup.cfg
Path("setup.cfg").unlink()
# {% elif cookiecutter.linting_and_formatting == "flake8+black+isort" %}
packages_to_install += flake8_black_isort
# {% endif %}
# track packages that are not available through conda
pip_only_packages = [
    "awscli",
    "python-dotenv",
]

# Select testing framework
tests_path = Path("tests")

# {% if cookiecutter.testing_framework == "pytest" %}
packages_to_install += ["pytest"]
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
packages_to_install += ["{{ cookiecutter.docs }}"]
pip_only_packages += ["{{ cookiecutter.docs }}"]
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

# Dev dependencies file handling:
# - conda: uses environment.yml (delete requirements-dev.txt)
# - uv: uses pyproject.toml [project.optional-dependencies.dev] (delete requirements-dev.txt)
# - virtualenv: uses requirements-dev.txt (keep it)
# {% if cookiecutter.environment_manager in ["conda", "uv", "none"] %}
Path("requirements-dev.txt").unlink(missing_ok=True)
# {% endif %}

# {% if cookiecutter.dependency_file != "environment.yml" %}
write_dependencies(
    "{{ cookiecutter.dependency_file }}",
    packages_to_install,
    pip_only_packages,
    repo_name="{{ cookiecutter.repo_name }}",
    module_name="{{ cookiecutter.module_name }}",
    python_version="{{ cookiecutter.python_version_number }}",
    environment_manager="{{ cookiecutter.environment_manager }}",
    description="{{ cookiecutter.description }}",
)
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
