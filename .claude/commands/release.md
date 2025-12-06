# Release Command

Release a new version of the cookiecutter-data-science template.

## Instructions

1. Read the current journal to get the latest entry number from `.claude/JOURNAL.md`
2. Update `pyproject.toml` version to `2.3.0+stellars<journal_number>`
3. Delete the old tag if it exists (both local and remote)
4. Commit the version change with message: `chore: bump version to 2.3.0+stellars<journal_number>`
5. Create new tag `v2.3.0+stellars<journal_number>`
6. Push commit and tag to origin

## Parameters

- `$ARGUMENTS` - Optional: specific journal number to use (if not provided, read from journal)

## Example

```
/release 48
```

This will create version `2.3.0+stellars48` and tag `v2.3.0+stellars48`.
