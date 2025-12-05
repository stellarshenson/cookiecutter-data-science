# Copier Support Analysis

This document captures research and implementation attempts on making this cookiecutter template interoperable with Copier.

## Overview

Copier is an alternative project templating tool with features like template updates and different syntax conventions. This analysis explores what would be required to support both cookiecutter and Copier from the same template.

## Implementation Attempt Summary

An experimental implementation was attempted on the `feature/copier-template` branch. Key findings:

### What Worked

1. **Cookiecutter namespace compatibility**: Copier can create a computed `cookiecutter` dict variable that allows `{{ cookiecutter.var }}` syntax to work in templates
2. **Jinja2 time extension**: Adding `jinja2_time.TimeExtension` allows the `{% now %}` tag to work
3. **Post-generation tasks**: Copier tasks can pass environment variables to Python scripts for cleanup
4. **Template rendering**: All Jinja2 templates rendered correctly with the cookiecutter namespace

### What Failed

**Critical blocker**: Cookiecutter requires the template directory to have a templated name containing `{{ cookiecutter.` (e.g., `{{ cookiecutter.repo_name }}/`). When renamed to `template/` for Copier compatibility, cookiecutter throws `NonTemplatedInputDirException`.

This is a fundamental architectural incompatibility - the same template directory cannot serve both tools.

## Current Template Features

Features that need Copier equivalents:

| Feature | Cookiecutter Implementation | Copier Consideration |
|---------|----------------------------|---------------------|
| Environment managers | Choice: uv, conda, virtualenv, none | Simple choice question |
| Dependency files | Choice: pyproject.toml, requirements.txt, environment.yml | Conditional on env manager |
| Cloud storage | Nested dict with subfields (s3.bucket, azure.container) | Copier supports nested questions |
| Jupyter kernel | Yes/No choice | Simple boolean |
| .env encryption | Yes/No with Makefile targets | Simple boolean |
| Build versioning | Auto-increment in pyproject.toml | Works unchanged |
| Dev/prod separation | Conditional file generation | Copier `_exclude` or tasks |
| Post-gen cleanup | hooks/post_gen_project.py | Copier `_tasks` |

## Key Differences

| Aspect | Cookiecutter | Copier |
|--------|--------------|--------|
| Config file | `cookiecutter.json` / `ccds.json` | `copier.yml` |
| Variable syntax | `{{ cookiecutter.var }}` | `{{ var }}` |
| Directory names | `{{ cookiecutter.repo_name }}/` (required) | `{{ repo_name }}/` or static |
| Hooks | `hooks/post_gen_project.py` (Jinja-rendered) | `_tasks` in copier.yml (static Python) |
| Template updates | Not supported | Native support |
| Conditional questions | Custom pre_prompt.py | Native `when:` clause |

## Challenges

### 1. Template Directory Name (Blocker)

Cookiecutter requires the template directory to contain `{{ cookiecutter.` in its name. Copier cannot process directories with this naming pattern correctly.

**Impact**: Fundamental incompatibility - cannot have single template directory for both tools.

### 2. Hook Files Are Jinja Templates

Cookiecutter's `hooks/post_gen_project.py` contains embedded Jinja2 variables (like `{{ cookiecutter.testing_framework }}`). Cookiecutter renders these before execution. Copier runs the raw Python file.

**Solution found**: Create separate `scripts/copier_post_gen.py` that reads configuration from environment variables passed via `_tasks`.

### 3. Nested Options (dataset_storage)

Our `dataset_storage` option uses nested dicts:
```json
{"s3": {"bucket": "bucket-name", "aws_profile": "default"}}
```

Copier handles this differently with separate questions and `when:` clauses.

**Solution found**: Flatten to separate questions (s3_bucket, azure_container, etc.) with conditional display.

## Potential Solutions

### Option 1: Separate Copier Template (Recommended)

Maintain a separate `copier/` directory with:
- `copier.yml` configuration
- Symlinks or copies of template files
- Dedicated post-gen script

**Pros**: Clean separation, both tools fully supported
**Cons**: Duplication, maintenance burden

### Option 2: Build-Time Generation

Maintain single source templates with a build script that generates both cookiecutter and Copier versions.

**Pros**: Single source of truth
**Cons**: Build step required, more complex CI/CD

### Option 3: Copier-Only Migration

Migrate entirely to Copier, abandoning cookiecutter support.

**Pros**: Simpler maintenance, template update support
**Cons**: Breaking change for existing users, loss of ccds CLI benefits

## Copier Advantages

If we did support Copier:

- **Template updates**: `copier update` applies template changes to existing projects
- **Native conditionals**: `when:` clause is cleaner than our pre_prompt.py filtering
- **Answer file**: `.copier-answers.yml` tracks choices for updates
- **Migrations**: Version-aware template updates with migration scripts

## Decision

**Status**: Not implementing Copier support at this time.

**Rationale**:
- The `{{ cookiecutter.repo_name }}/` directory naming requirement is a fundamental blocker
- Current cookiecutter setup works well with `ccds` CLI
- Template is already standalone and doesn't require ccds package internals
- Copier support would require maintaining parallel template structures
- All current features (env encryption, build versioning, etc.) work well with cookiecutter

## Experimental Code

The implementation attempt included:

1. `copier.yml` with all questions and computed `cookiecutter` namespace
2. `scripts/copier_post_gen.py` that reads env vars for cleanup
3. `jinja2_time.TimeExtension` for `{% now %}` tag support

This code worked for Copier but was removed due to the directory naming blocker that breaks cookiecutter compatibility.

## Future Considerations

If Copier support becomes desired:

1. Create separate `copier/` directory with template copy
2. Maintain `copier.yml` alongside `ccds.json`
3. Use shared template files via symlinks where possible
4. Implement parallel test suites

## References

- [Copier Documentation](https://copier.readthedocs.io/)
- [Copier Jinja2 Extensions](https://copier.readthedocs.io/en/stable/configuring/#jinja_extensions)
- [Cookiecutter to Copier Migration](https://copier.readthedocs.io/en/stable/comparisons/)
- [Cookiecutter find_template source](https://github.com/cookiecutter/cookiecutter/blob/main/cookiecutter/find.py)
