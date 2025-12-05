# Copier Support

This template supports both [Cookiecutter](https://cookiecutter.readthedocs.io/) and [Copier](https://copier.readthedocs.io/) for project generation.

## Why Copier?

Copier offers features not available in Cookiecutter:

- **Template updates** - `copier update` applies template changes to existing projects
- **Answer tracking** - `.copier-answers.yml` records choices for reproducibility
- **Native conditionals** - `when:` clause for cleaner question flow
- **Migrations** - Version-aware template updates with migration scripts

## Quick Start

### Using Cookiecutter (default)

```bash
ccds gh:stellarshenson/cookiecutter-data-science
```

### Using Copier

```bash
# Clone the repository first (required - copier doesn't support subdirectory paths in Git URLs)
git clone https://github.com/stellarshenson/cookiecutter-data-science.git

# Create project from local clone
copier copy --trust ./cookiecutter-data-science/copier my-project

# With pre-filled answers (non-interactive)
copier copy --trust ./cookiecutter-data-science/copier \
  -d project_name="My Project" \
  -d environment_manager="conda" \
  my-project
```

The `--trust` flag is required because the template uses Jinja extensions and post-generation tasks.

## Updating Projects

One of Copier's key advantages is updating existing projects when the template changes:

```bash
cd my-existing-project
copier update --trust
```

This will:
1. Read `.copier-answers.yml` to recall your original choices
2. Apply template changes while preserving your modifications
3. Show conflicts for manual resolution if needed

## Architecture

The template maintains two parallel structures:

```
cookiecutter-data-science/
├── {{ cookiecutter.repo_name }}/    # Cookiecutter template (source of truth)
├── ccds.json                        # Cookiecutter configuration
├── hooks/post_gen_project.py        # Cookiecutter post-gen hook
└── copier/                          # Copier template (derived)
    ├── copier.yml                   # Copier configuration
    ├── template/                    # Transformed template files
    └── scripts/
        ├── build_copier_template.py # Transforms cookiecutter -> copier
        └── copier_post_gen.py       # Post-gen cleanup script
```

The Cookiecutter template is the **source of truth**. The Copier template is generated from it using a build script.

## Build Process

After modifying cookiecutter template files, regenerate the Copier template:

```bash
python copier/scripts/build_copier_template.py
```

This script:
1. Copies `{{ cookiecutter.repo_name }}/` to `copier/template/`
2. Transforms `{{ cookiecutter.var }}` syntax to `{{ var }}`
3. Flattens nested `dataset_storage` dict to individual variables
4. Renames templated directory/file names

## Key Differences

| Aspect | Cookiecutter | Copier |
|--------|--------------|--------|
| Config file | `ccds.json` | `copier/copier.yml` |
| Variable syntax | `{{ cookiecutter.var }}` | `{{ var }}` |
| Template directory | `{{ cookiecutter.repo_name }}/` | `copier/template/` |
| Post-gen hook | Jinja-rendered Python | Static Python with CLI args |
| Cloud storage | Nested dict | Flat variables with `when:` |
| Template updates | Not supported | `copier update` |

## Dataset Storage Variables

Cookiecutter uses nested dicts:
```json
{"s3": {"bucket": "my-bucket", "aws_profile": "default"}}
```

Copier uses flat questions with conditionals:

| Copier Variable | Cookiecutter Equivalent |
|-----------------|------------------------|
| `dataset_storage` | Choice: none, s3, azure, gcs |
| `s3_bucket` | `dataset_storage.s3.bucket` |
| `s3_aws_profile` | `dataset_storage.s3.aws_profile` |
| `azure_container` | `dataset_storage.azure.container` |
| `gcs_bucket` | `dataset_storage.gcs.bucket` |

## Development Workflow

1. Make changes to the cookiecutter template in `{{ cookiecutter.repo_name }}/`
2. Run `python copier/scripts/build_copier_template.py`
3. Test both:
   ```bash
   # Test cookiecutter
   cookiecutter . -o /tmp/test-cc --no-input

   # Test copier
   copier copy --trust ./copier /tmp/test-copier --defaults
   ```
4. Commit both the cookiecutter changes and regenerated Copier template

## Technical Notes

### How Cookiecutter and Copier Work in Tandem

Both template systems produce identical projects from a single source of truth - the cookiecutter template. The process works as follows:

**Template Synchronization:**
1. The cookiecutter template (`{{ cookiecutter.repo_name }}/`) is the authoritative source
2. Running `build_copier_template.py` transforms it to copier format in `copier/template/`
3. The build script handles syntax conversion (`{{ cookiecutter.var }}` -> `{{ var }}`), directory renaming, and variable flattening

**File Generation Parity:**
- Both templates use the same `env_matrix.py` for file expectations in tests
- Generated projects contain identical files (except `.copier-answers.yml` for Copier)
- Post-generation cleanup is equivalent - same files removed based on configuration choices

**Testing Strategy:**
- `tests/test_creation.py` - Tests cookiecutter template (24 configurations)
- `tests/test_copier.py` - Tests copier template (25 configurations including answers file test)
- Both test suites use `env_matrix.py` to verify correct file generation
- Running both ensures changes don't break either template system

### Post-Generation Script

Cookiecutter's hook (`hooks/post_gen_project.py`) is a Jinja template - variables like `{{ cookiecutter.testing_framework }}` are rendered before execution.

Copier's tasks run static Python (`copier/scripts/copier_post_gen.py`), so the post-gen script receives configuration via command-line arguments passed from `copier.yml`:

```yaml
_tasks:
  - >-
    python3 "{{ _copier_conf.src_path }}/scripts/copier_post_gen.py"
    --testing-framework "{{ testing_framework }}"
    --linting-and-formatting "{{ linting_and_formatting }}"
    # ... all other configuration arguments
```

Both scripts perform identical cleanup operations:
- Remove files based on `linting_and_formatting` choice (e.g., `setup.cfg` for ruff)
- Move selected testing framework files to `tests/`
- Move selected docs framework files to `docs/`
- Remove unused dependency files based on `dependency_file` choice
- Write Python version to `pyproject.toml`
- Apply custom config overlay if provided

### Template Suffix

The `_templates_suffix: ""` setting processes all files as Jinja templates, matching Cookiecutter's behavior. This means `.jinja` extensions are not stripped automatically - the post-gen script handles renaming `.copier-answers.yml.jinja` to `.copier-answers.yml`.

### Answers File

The `.copier-answers.yml` file is generated from a template (`copier/template/.copier-answers.yml.jinja`) that uses the special `_copier_answers` variable:

```yaml+jinja
# Changes here will be overwritten by Copier; NEVER EDIT MANUALLY
{{ _copier_answers|to_nice_yaml -}}
```

This file enables `copier update` to recall user choices when updating projects to newer template versions.

### Jinja Extensions

Both tools use `jinja2_time.TimeExtension` for the `{% now %}` tag in LICENSE files.
