#!/usr/bin/env python3
"""
Build script to transform cookiecutter templates to copier format.

This script:
1. Copies the cookiecutter template directory to copier/template/
2. Renames {{ cookiecutter.repo_name }} to {{ repo_name }}
3. Transforms {{ cookiecutter.var }} to {{ var }} in all template files
4. Transforms nested dataset_storage dict to flat variables

Run this script whenever the cookiecutter templates change.
"""
import re
import shutil
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
COOKIECUTTER_TEMPLATE = REPO_ROOT / "{{ cookiecutter.repo_name }}"
COPIER_TEMPLATE = SCRIPT_DIR.parent / "template"


def transform_cookiecutter_to_copier(content: str) -> str:
    """Transform cookiecutter Jinja2 syntax to copier syntax."""

    # Step 1: Transform dataset_storage nested dict patterns BEFORE removing cookiecutter. prefix
    # This is critical - we need to handle the complex nested structures first

    # Transform value access patterns:
    # {{ cookiecutter.dataset_storage.s3.bucket }} -> {{ s3_bucket }}
    # {{ cookiecutter.dataset_storage.s3.aws_profile }} -> {{ s3_aws_profile }}
    # {{ cookiecutter.dataset_storage.azure.container }} -> {{ azure_container }}
    # {{ cookiecutter.dataset_storage.gcs.bucket }} -> {{ gcs_bucket }}
    content = re.sub(
        r"\{\{\s*cookiecutter\.dataset_storage\.s3\.bucket\s*\}\}",
        "{{ s3_bucket }}",
        content,
    )
    content = re.sub(
        r"\{\{\s*cookiecutter\.dataset_storage\.s3\.aws_profile\s*\}\}",
        "{{ s3_aws_profile }}",
        content,
    )
    content = re.sub(
        r"\{\{\s*cookiecutter\.dataset_storage\.azure\.container\s*\}\}",
        "{{ azure_container }}",
        content,
    )
    content = re.sub(
        r"\{\{\s*cookiecutter\.dataset_storage\.gcs\.bucket\s*\}\}",
        "{{ gcs_bucket }}",
        content,
    )

    # Transform conditional check patterns (in if/elif statements):
    # {%- if cookiecutter.dataset_storage.s3 %} -> {%- if dataset_storage == 's3' %}
    # {%- if cookiecutter.dataset_storage.azure %} -> {%- if dataset_storage == 'azure' %}
    # {%- if cookiecutter.dataset_storage.gcs %} -> {%- if dataset_storage == 'gcs' %}
    # {%- if cookiecutter.dataset_storage.none %} -> {%- if dataset_storage == 'none' %}
    # {%- if not cookiecutter.dataset_storage.none %} -> {%- if dataset_storage != 'none' %}
    content = re.sub(
        r"\{%[-]?\s*if\s+not\s+cookiecutter\.dataset_storage\.none\s*%\}",
        "{% if dataset_storage != 'none' %}",
        content,
    )
    content = re.sub(
        r"\{%[-]?\s*if\s+cookiecutter\.dataset_storage\.(s3|azure|gcs|none)\s*%\}",
        r"{% if dataset_storage == '\1' %}",
        content,
    )
    content = re.sub(
        r"\{%[-]?\s*elif\s+cookiecutter\.dataset_storage\.(s3|azure|gcs|none)\s*%\}",
        r"{% elif dataset_storage == '\1' %}",
        content,
    )

    # Transform comparison patterns (e.g., aws_profile != 'default'):
    # {%- if cookiecutter.dataset_storage.s3.aws_profile != 'default' %}
    # -> {%- if s3_aws_profile != 'default' %}
    content = re.sub(
        r"\{%[-]?\s*if\s+cookiecutter\.dataset_storage\.s3\.aws_profile\s*!=\s*['\"]default['\"]\s*%\}",
        "{% if s3_aws_profile != 'default' %}",
        content,
    )

    # Step 2: Now transform all remaining {{ cookiecutter.var }} to {{ var }}
    content = re.sub(r"\{\{\s*cookiecutter\.(\w+)\s*\}\}", r"{{ \1 }}", content)

    # Step 3: Transform if/elif statements with cookiecutter.var
    content = re.sub(
        r"\{%[-]?\s*if\s+cookiecutter\.(\w+)", r"{% if \1", content
    )
    content = re.sub(
        r"\{%[-]?\s*elif\s+cookiecutter\.(\w+)", r"{% elif \1", content
    )

    # Step 4: Handle any remaining cookiecutter.var in expressions
    content = re.sub(r"cookiecutter\.(\w+)", r"\1", content)

    return content


def transform_filename(name: str) -> str:
    """Transform cookiecutter filename syntax to copier syntax."""
    # Replace {{ cookiecutter.var }} with {{ var }}
    return re.sub(r"\{\{\s*cookiecutter\.(\w+)\s*\}\}", r"{{ \1 }}", name)


def copy_and_transform_tree(src: Path, dst: Path):
    """Recursively copy and transform directory tree."""
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    for item in src.iterdir():
        # Transform the name
        new_name = transform_filename(item.name)
        dst_item = dst / new_name

        if item.is_dir():
            copy_and_transform_tree(item, dst_item)
        else:
            # Check if it's a text file we should transform
            try:
                content = item.read_text(encoding="utf-8")
                transformed = transform_cookiecutter_to_copier(content)
                dst_item.write_text(transformed, encoding="utf-8")
                print(f"  Transformed: {item.name} -> {new_name}")
            except UnicodeDecodeError:
                # Binary file, just copy
                shutil.copy2(item, dst_item)
                print(f"  Copied (binary): {item.name} -> {new_name}")


def main():
    print("Building Copier template from Cookiecutter source...")
    print(f"  Source: {COOKIECUTTER_TEMPLATE}")
    print(f"  Destination: {COPIER_TEMPLATE}")
    print()

    if not COOKIECUTTER_TEMPLATE.exists():
        print(f"ERROR: Source directory not found: {COOKIECUTTER_TEMPLATE}")
        return 1

    copy_and_transform_tree(COOKIECUTTER_TEMPLATE, COPIER_TEMPLATE)

    print()
    print("Done! Copier template created at:", COPIER_TEMPLATE)
    return 0


if __name__ == "__main__":
    exit(main())
