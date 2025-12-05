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
# From local clone
copier copy --trust ./copier my-project

# From GitHub (main branch)
copier copy --trust "https://github.com/stellarshenson/cookiecutter-data-science.git//copier" my-project

# From specific branch
copier copy --trust "https://github.com/stellarshenson/cookiecutter-data-science.git//copier" --vcs-ref feature/copier-template my-project
```

The `--trust` flag is required because the template uses Jinja extensions and post-generation tasks. The `//copier` suffix tells Copier to look in the `copier/` subdirectory.

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

### Post-Generation Script

Cookiecutter's hook is a Jinja template - variables like `{{ cookiecutter.testing_framework }}` are rendered before execution.

Copier's tasks run static Python, so the post-gen script receives configuration via command-line arguments.

### Template Suffix

The `_templates_suffix: ""` setting processes all files as Jinja templates, matching Cookiecutter's behavior.

### Jinja Extensions

Both tools use `jinja2_time.TimeExtension` for the `{% now %}` tag in LICENSE files.
