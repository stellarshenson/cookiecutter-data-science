# Release Command

Release a new version of the cookiecutter-data-science template.

## Instructions

1. Read the current journal to get the latest entry number from `.claude/JOURNAL.md`
2. **CRITICAL**: The stellars number MUST match the latest journal entry number. If journal ends at entry 55, release must be `stellars55`. Before releasing, verify journal entry number matches intended release number. If they don't match, update journal first to add entries or split existing entries.
3. Update `pyproject.toml` version to `2.3.0+stellars<journal_number>`
4. Commit the version change with message: `chore: bump version to 2.3.0+stellars<journal_number>`
5. Create new tag `v2.3.0+stellars<journal_number>`
6. Push commit and tag to origin

**IMPORTANT**: Do NOT delete old tags - they are needed for `copier update` to work on existing projects.

**IMPORTANT**: Journal entry number and stellars release number must always be in sync. One journal entry = one potential release.

## Parameters

- `$ARGUMENTS` - Optional: specific journal number to use (if not provided, read from journal)

## Example

```
/release 48
```

This will create version `2.3.0+stellars48` and tag `v2.3.0+stellars48`.
