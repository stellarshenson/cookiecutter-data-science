# Release Command

Release a new version of the cookiecutter-data-science template.

## Instructions

1. Read `.claude/JOURNAL.md` and find the **last entry number** (e.g., if last entry is `55. **Task - ...`, the number is 55)
2. Update `pyproject.toml` version to `2.3.0+stellars<last_journal_entry_number>`
3. Commit the version change with message: `chore: bump version to 2.3.0+stellars<last_journal_entry_number>`
4. Create new tag `v2.3.0+stellars<last_journal_entry_number>`
5. Push commit and tag to origin

**IMPORTANT**: Do NOT delete old tags - they are needed for `copier update` to work on existing projects.

**IMPORTANT**: The release number is ALWAYS derived from the last journal entry number. If journal ends at 55, release is stellars55. No exceptions.
