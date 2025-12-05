# Copier Support

This template now supports both Cookiecutter and Copier for project generation.

## Quick Start

### Using Cookiecutter (default)

```bash
# Via ccds CLI
ccds https://github.com/stellarshenson/cookiecutter-data-science

# Or directly with cookiecutter
cookiecutter https://github.com/stellarshenson/cookiecutter-data-science
```

### Using Copier

```bash
# From local clone
copier copy --trust ./copier my-project --defaults

# From GitHub (main branch)
copier copy --trust "https://github.com/stellarshenson/cookiecutter-data-science.git//copier" my-project

# From specific branch
copier copy --trust "https://github.com/stellarshenson/cookiecutter-data-science.git//copier" --vcs-ref feature/copier-template my-project
```

The `--trust` flag is required because the template uses Jinja extensions and post-generation tasks. The `//copier` suffix tells copier to look in the `copier/` subdirectory.

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

### Build Process

The Copier template is generated from the Cookiecutter source using:

```bash
python copier/scripts/build_copier_template.py
```

This script:
1. Copies `{{ cookiecutter.repo_name }}/` to `copier/template/`
2. Transforms `{{ cookiecutter.var }}` syntax to `{{ var }}`
3. Flattens nested `dataset_storage` dict to individual variables
4. Renames templated directory/file names

**Run this script after modifying the cookiecutter template files.**

## Key Differences

| Aspect | Cookiecutter | Copier |
|--------|--------------|--------|
| Config file | `ccds.json` | `copier/copier.yml` |
| Variable syntax | `{{ cookiecutter.var }}` | `{{ var }}` |
| Template directory | `{{ cookiecutter.repo_name }}/` | `copier/template/` |
| Post-gen hook | `hooks/post_gen_project.py` (Jinja-rendered) | `copier/scripts/copier_post_gen.py` (CLI args) |
| Cloud storage | Nested dict: `dataset_storage.s3.bucket` | Flat: `s3_bucket`, `azure_container` |
| Template updates | Not supported | `copier update` |

## Dataset Storage Mapping

Cookiecutter uses nested dicts for cloud storage configuration:

```json
{"s3": {"bucket": "my-bucket", "aws_profile": "default"}}
```

Copier uses flat questions with `when:` conditionals:

| Copier Variable | Maps To |
|-----------------|---------|
| `dataset_storage` | Choice: none, s3, azure, gcs |
| `s3_bucket` | `dataset_storage.s3.bucket` |
| `s3_aws_profile` | `dataset_storage.s3.aws_profile` |
| `azure_container` | `dataset_storage.azure.container` |
| `gcs_bucket` | `dataset_storage.gcs.bucket` |

## Copier Advantages

- **Template updates**: `copier update` applies template changes to existing projects
- **Native conditionals**: `when:` clause for cleaner question flow
- **Answer file**: `.copier-answers.yml` tracks choices for reproducibility
- **Migrations**: Version-aware template updates with migration scripts

## Development Workflow

1. Make changes to the cookiecutter template in `{{ cookiecutter.repo_name }}/`
2. Run `python copier/scripts/build_copier_template.py` to regenerate Copier template
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

Cookiecutter's hook (`hooks/post_gen_project.py`) is a Jinja template itself - variables like `{{ cookiecutter.testing_framework }}` are rendered before execution.

Copier's tasks run static Python files, so `copier/scripts/copier_post_gen.py` receives configuration via command-line arguments passed from `copier.yml`.

### Template Suffix

The `_templates_suffix: ""` setting in `copier.yml` tells Copier to process all files as Jinja templates, not just `.jinja` files. This matches cookiecutter's behavior.

### Jinja Extensions

Both tools use `jinja2_time.TimeExtension` for the `{% now %}` tag in LICENSE files.

## References

- [Copier Documentation](https://copier.readthedocs.io/)
- [Copier Configuring Templates](https://copier.readthedocs.io/en/stable/configuring/)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
