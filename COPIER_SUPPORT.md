# Copier Support Analysis

This document captures research on making this cookiecutter template interoperable with Copier.

## Overview

Copier is an alternative project templating tool with features like template updates and different syntax conventions. This analysis explores what would be required to support both cookiecutter and Copier from the same template.

## Key Differences

| Aspect | Cookiecutter | Copier |
|--------|--------------|--------|
| Config file | `cookiecutter.json` / `ccds.json` | `copier.yml` |
| Variable syntax | `{{ cookiecutter.var }}` | `{{ var }}` |
| Directory names | `{{ cookiecutter.repo_name }}/` | `{{ repo_name }}/` |
| Hooks | `hooks/post_gen_project.py` | `_tasks` in copier.yml |
| Template updates | Not supported | Native support |

## Challenges

### 1. Variable Namespace

All templates in this repo use `{{ cookiecutter.variable }}` syntax. Copier uses `{{ variable }}` directly without a namespace prefix.

**Impact**: Every template file would need modification, or a compatibility layer.

### 2. Template Directory Name

The template directory is named `{{ cookiecutter.repo_name }}/`. Copier processes directory names with its own syntax.

**Impact**: Directory would need renaming or special handling.

### 3. Hooks vs Tasks

Cookiecutter uses Python hooks in `hooks/post_gen_project.py`. Copier uses `_tasks` defined in YAML with shell commands or Python scripts.

**Impact**: Hook logic would need to be rewritten or adapted.

## Potential Solutions

### Option 1: Copier Compatibility Mode (Low Effort)

Copier has partial cookiecutter compatibility but struggles with the `cookiecutter.` namespace.

**Verdict**: Insufficient for this template's complexity.

### Option 2: Dual Config with Namespace Alias (Medium Effort)

Add `copier.yml` alongside existing config. Define a computed `cookiecutter` dict:

```yaml
# copier.yml
repo_name:
  type: str
  help: Repository name

module_name:
  type: str
  help: Module name

# Create cookiecutter namespace as computed value
cookiecutter:
  type: json
  default: |
    {
      "repo_name": "{{ repo_name }}",
      "module_name": "{{ module_name }}",
      "environment_manager": "{{ environment_manager }}"
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

1. Rename `{{ cookiecutter.repo_name }}/` to `{{ repo_name }}/`
2. Add `copier.yml` with all questions
3. Define `cookiecutter` as computed dict in copier.yml
4. Existing template syntax works unchanged

**Pros**: Works for both tools with minimal changes
**Cons**: Cookiecutter requires the `cookiecutter.` prefix in directory names by default

## Decision

**Status**: Not implementing Copier support at this time.

**Rationale**:
- Current cookiecutter setup works well with `ccds` CLI
- Template is already standalone and doesn't require ccds package internals
- Copier support would add maintenance burden without clear user demand
- The `{{ cookiecutter.repo_name }}/` directory naming convention is deeply embedded

## Future Considerations

If Copier support becomes desired:

1. Start with Option 5 (rename directory + computed namespace)
2. Test thoroughly with both `ccds` and `copier` CLIs
3. Adapt hooks to work as Copier tasks
4. Maintain parallel test suites

## References

- [Copier Documentation](https://copier.readthedocs.io/)
- [Copier Jinja2 Extensions](https://copier.readthedocs.io/en/stable/configuring/#jinja_extensions)
- [Cookiecutter to Copier Migration](https://copier.readthedocs.io/en/stable/comparisons/)
