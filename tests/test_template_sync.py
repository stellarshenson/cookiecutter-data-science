"""
Test that copier template is in sync with cookiecutter source.

This test should run first to catch sync issues early.
The cookiecutter template is the master, copier template is derived.
"""

import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parents[1].resolve()
COOKIECUTTER_TEMPLATE = REPO_ROOT / "{{ cookiecutter.repo_name }}"
COPIER_TEMPLATE = REPO_ROOT / "copier" / "template"
BUILD_SCRIPT = REPO_ROOT / "copier" / "scripts" / "build_copier_template.py"


def compare_directories(dir1: Path, dir2: Path, ignore: list = None) -> list:
    """Recursively compare two directories and return list of differences."""
    ignore = ignore or []
    differences = []

    # Get all files in both directories
    files1 = set(p.relative_to(dir1) for p in dir1.rglob("*") if p.is_file())
    files2 = set(p.relative_to(dir2) for p in dir2.rglob("*") if p.is_file())

    # Filter out ignored files
    files1 = {f for f in files1 if f.name not in ignore}
    files2 = {f for f in files2 if f.name not in ignore}

    # Files only in dir1
    for f in files1 - files2:
        differences.append(f"Only in {dir1.name}: {f}")

    # Files only in dir2
    for f in files2 - files1:
        differences.append(f"Only in {dir2.name}: {f}")

    # Compare common files
    for f in files1 & files2:
        file1 = dir1 / f
        file2 = dir2 / f
        try:
            if file1.read_text() != file2.read_text():
                differences.append(f"Content differs: {f}")
        except UnicodeDecodeError:
            # Binary files - compare bytes
            if file1.read_bytes() != file2.read_bytes():
                differences.append(f"Binary content differs: {f}")

    return differences


class TestTemplateSync:
    """Test that copier template stays in sync with cookiecutter source."""

    def test_copier_template_in_sync(self):
        """
        Verify copier template matches what build script would generate.

        This test regenerates the copier template to a temp directory and
        compares it with the committed copier/template/. If they differ,
        the developer forgot to run build_copier_template.py before committing.
        """
        # Generate fresh copier template to temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_template = Path(tmpdir) / "template"

            # Run the build script with modified output path
            # We'll import and call the function directly
            import sys

            sys.path.insert(0, str(BUILD_SCRIPT.parent))
            from build_copier_template import copy_and_transform_tree

            copy_and_transform_tree(COOKIECUTTER_TEMPLATE, tmp_template)

            # Compare with committed copier template
            # Ignore .copier-answers.yml.jinja as it's copier-specific
            differences = compare_directories(
                tmp_template,
                COPIER_TEMPLATE,
                ignore=[".copier-answers.yml.jinja"],
            )

            if differences:
                diff_msg = "\n".join(differences[:20])  # Show first 20
                pytest.fail(
                    f"Copier template is out of sync with cookiecutter source!\n"
                    f"Run: python copier/scripts/build_copier_template.py\n\n"
                    f"Differences:\n{diff_msg}"
                )

    def test_build_script_exists(self):
        """Verify the build script exists."""
        assert BUILD_SCRIPT.exists(), f"Build script not found: {BUILD_SCRIPT}"

    def test_copier_template_exists(self):
        """Verify copier template directory exists."""
        assert COPIER_TEMPLATE.exists(), f"Copier template not found: {COPIER_TEMPLATE}"

    def test_cookiecutter_template_exists(self):
        """Verify cookiecutter template directory exists."""
        assert (
            COOKIECUTTER_TEMPLATE.exists()
        ), f"Cookiecutter template not found: {COOKIECUTTER_TEMPLATE}"
