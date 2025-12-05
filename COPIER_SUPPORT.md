# Copier Support Analysis

This document captures research on making this cookiecutter template interoperable with Copier.

## Overview

Copier is an alternative project templating tool with features like template updates and different syntax conventions. This analysis explores what would be required to support both cookiecutter and Copier from the same template.

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
| Directory names | `{{ cookiecutter.repo_name }}/` | `{{ repo_name }}/` |
| Hooks | `hooks/post_gen_project.py` | `_tasks` in copier.yml |
| Template updates | Not supported | Native support |
| Conditional questions | Custom pre_prompt.py | Native `when:` clause |

## Challenges

### 1. Variable Namespace

All templates use `{{ cookiecutter.variable }}` syntax. Copier uses `{{ variable }}` directly.

**Impact**: Every template file would need modification, or a compatibility layer.

### 2. Template Directory Name

The template directory is named `{{ cookiecutter.repo_name }}/`. Copier processes directory names with its own syntax.

**Impact**: Directory would need renaming or special handling.

### 3. Hooks vs Tasks

Cookiecutter uses Python hooks in `hooks/post_gen_project.py`. Our hook handles:
- File cleanup based on environment manager and dependency file
- Conditional deletion of requirements.txt, requirements-dev.txt, environment.yml
- License file selection
- Test framework setup

Copier uses `_tasks` defined in YAML with shell commands or Jinja templates.

**Impact**: Hook logic would need to be rewritten as tasks.

### 4. Nested Options (dataset_storage)

Our `dataset_storage` option uses nested dicts:
```json
{"s3": {"bucket": "bucket-name", "aws_profile": "default"}}
```

Copier handles this differently with conditional questions using `when:` clauses.

### 5. Conditional Option Display (env_location, dependency_file)

Our `pre_prompt.py` filters options based on previous answers:
- `env_location` only shown for conda
- `environment.yml` only available for conda

Copier handles this natively with `when:` clauses - actually simpler.

## Potential Solutions

### Option 1: Copier Compatibility Mode (Low Effort)

Copier has partial cookiecutter compatibility but struggles with the `cookiecutter.` namespace.

**Verdict**: Insufficient for this template's complexity.

### Option 2: Dual Config with Namespace Alias (Medium Effort)

Add `copier.yml` alongside existing config. Define a computed `cookiecutter` dict:

```yaml
# copier.yml
_subdirectory: template

repo_name:
  type: str
  help: Repository name

module_name:
  type: str
  default: "lib_{{ repo_name | replace('-', '_') }}"
  help: Module name (lib_ prefix)

environment_manager:
  type: str
  choices:
    - uv
    - conda
    - virtualenv
    - none
  default: uv

env_location:
  type: str
  choices:
    - local
    - global
  default: local
  when: "{{ environment_manager == 'conda' }}"

env_encryption:
  type: bool
  default: true
  help: Enable .env encryption (OpenSSL AES-256)

# Create cookiecutter namespace as computed value
cookiecutter:
  type: json
  default: |
    {
      "repo_name": "{{ repo_name }}",
      "module_name": "{{ module_name }}",
      "environment_manager": "{{ environment_manager }}",
      "env_encryption": "{{ 'Yes' if env_encryption else 'No' }}"
    }
```

**Pros**: Minimal template changes
**Cons**: Requires maintaining parallel configs, directory name still problematic

### Option 3: Jinja2 Extension (Medium Effort)

Use Copier's `_jinja_extensions` to inject a `cookiecutter` namespace:

```yaml
_jinja_extensions:
  - extensions/cookiecutter_compat.py:CookiecutterCompat
```

**Pros**: Clean separation, templates unchanged
**Cons**: Additional complexity, needs custom extension code

### Option 4: Build-Time Generation (Medium-High Effort)

Maintain single source templates with a build script that generates both cookiecutter and Copier versions.

**Pros**: Single source of truth, most maintainable long-term
**Cons**: Build step required, more complex CI/CD

### Option 5: Rename Directory + Computed Namespace (Recommended if Pursued)

1. Rename `{{ cookiecutter.repo_name }}/` to `template/` with `_subdirectory: template`
2. Add `copier.yml` with all questions
3. Define `cookiecutter` as computed dict in copier.yml
4. Existing template syntax works unchanged

**Pros**: Works for both tools with minimal changes
**Cons**: May break existing cookiecutter workflows

## Copier Advantages

If we did support Copier:

- **Template updates**: `copier update` applies template changes to existing projects
- **Native conditionals**: `when:` clause is cleaner than our pre_prompt.py filtering
- **Answer file**: `.copier-answers.yml` tracks choices for updates
- **Migrations**: Version-aware template updates with migration scripts

## Decision

**Status**: Not implementing Copier support at this time.

**Rationale**:
- Current cookiecutter setup works well with `ccds` CLI
- Template is already standalone and doesn't require ccds package internals
- Copier support would add maintenance burden without clear user demand
- The `{{ cookiecutter.repo_name }}/` directory naming convention is deeply embedded
- All current features (env encryption, build versioning, etc.) work well with cookiecutter

## Future Considerations

If Copier support becomes desired:

1. Start with Option 5 (subdirectory + computed namespace)
2. Convert pre_prompt.py conditionals to Copier `when:` clauses
3. Convert post_gen_project.py to Copier `_tasks`
4. Test thoroughly with both `ccds` and `copier` CLIs
5. Maintain parallel test suites

## References

- [Copier Documentation](https://copier.readthedocs.io/)
- [Copier Jinja2 Extensions](https://copier.readthedocs.io/en/stable/configuring/#jinja_extensions)
- [Cookiecutter to Copier Migration](https://copier.readthedocs.io/en/stable/comparisons/)
