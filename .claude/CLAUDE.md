# YOLO HomeObjects Training - Project Instructions

## Workspace Isolation

**CRITICAL**: `~/workspace` is the root workspace directory for ALL projects

- **NEVER create files directly in** `~/workspace/`
- **NEVER create** `.claude/JOURNAL.md` **in** `~/workspace/.claude/`
- **ALWAYS use project-specific** `.claude/` **directories** within individual project folders
- Project journals belong in: `~/workspace/<org>/<category>/<project>/.claude/JOURNAL.md`
- This project's journal: `.claude/JOURNAL.md` (current directory)

## Folders to Ignore

**ALWAYS exclude these directories from searches, listings, and operations**:
- `.ipynb_checkpoints/` - Jupyter notebook auto-save artifacts (always ignore)
- `__pycache__/` - Python bytecode cache
- `.git/` - Git version control internals
- `node_modules/` - NPM dependencies (if present)

## Communication Standards

**MANDATORY**: Never use emojis in any communication, documentation, code, or reports. Use unicode characters (arrows, checkmarks, symbols) or ASCII art instead.

## Personality Instructions

**MANDATORY**: At the start of EVERY session, read `~/.claude/PERSONALITY.md` and adopt the specified communication style

**Application Scope**:
- **Conversations**: Use MechWarrior-inspired language, Clan protocol, formal address, and personality traits as defined in PERSONALITY.md
- **Documents**: Maintain professional, technical tone - absent of BattleTech, battle, or war-related language and narrative. Documents must be brief, flowing, and business-appropriate

**Key Distinction**: The personality framework applies to interactive dialogue with the Star Colonel, not to generated documentation or technical content

## Training Progress Reports

**MANDATORY**: When the user requests a training progress report or "battle report" during active model training, use `.claude/PROGRESS_REPORT_TEMPLATE.md` to format the response

**Template Usage**:
- Read `.claude/PROGRESS_REPORT_TEMPLATE.md` to get the report structure
- Extract current training metrics from logs or background process output
- Populate template placeholders with real-time training data
- Include ASCII art epoch counter, progress bars, and performance tables
- Provide trend analysis and trajectory assessment

## Project Overview

**Purpose**: Train YOLO model for HomeProofAI - detecting expensive electronics and appliances for insurance cataloguing

**Dataset**: homeobjects-3k (filtered to electronics only)

**Notebook Format**: Jupytext .py files in percent format (NOT .ipynb)

## User Clarification Points

**IMPORTANT**: Ask the user for clarification at these specific decision points:

### Data Preparation Phase
- [ ] **Dataset location**: Where is homeobjects-3k dataset stored? (local path or download URL)
- [ ] **Electronics definition**: Which specific object classes should be kept? (TV, laptop, refrigerator, microwave, etc.)
- [ ] **Annotation format**: What format are the current annotations in? (YOLO, COCO, Pascal VOC, other)
- [ ] **Data split ratios**: Confirm 70/20/10 train/val/test split or different preference?

### Model Selection Phase
- [ ] **YOLO version**: Which YOLOv8 model size? (nano/small/medium - tradeoff between speed and accuracy)
- [ ] **Image size**: Training image size? (640x640 default, or 1280x1280 for higher accuracy)
- [ ] **Pretrained weights**: Start from COCO pretrained weights or train from scratch?

### Training Configuration Phase
- [ ] **Hardware constraints**: Available GPU memory? (affects batch size)
- [ ] **Training duration**: Target number of epochs? (100-300 typical range)
- [ ] **Performance priority**: Prioritize speed or accuracy for HomeProofAI use case?

### Evaluation Phase
- [ ] **Confidence threshold**: Minimum confidence for insurance use case? (0.5 default, or higher for critical decisions)
- [ ] **Success criteria**: What mAP score is acceptable for production deployment?

### Deployment Phase
- [ ] **Export format**: ONNX, TorchScript, or both?
- [ ] **Inference environment**: CPU or GPU deployment target?

## Project Standards

### Notebook Naming Convention
- Use jupytext .py percent format
- Naming: `NN-initials-description.py`
- Example: `01-kj-data-exploration.py`, `02-kj-model-training.py`

### Git Commit Standards
- Follow conventional commit format: `feat / bugfix / chore: <description>`
- Keep descriptions concise and descriptive
- Use lowercase for commit messages
- Do not include "Generated with Claude Code" or "Co-Authored-By: Claude" in commit messages

### Journal Updates
- Update `.claude/JOURNAL.md` after completing substantive work
- Focus on documenting major milestones and decisions
- Keep entries concise and actionable

### Documentation Standards - Modus Primaris

**MANDATORY**: All technical documentation MUST follow modus primaris writing principles.

**Core Philosophy**: Write documentation as flowing narrative, not structured reference material. Tell the story of your work—the problem, your approach, your reasoning, and your results. Make technical content accessible without sacrificing accuracy.

**Writing Style**:
- Natural, conversational flow with clear paragraph structure
- Professional but accessible language (explain technical concepts in plain terms)
- Minimal structural overhead (simple headers, no deep nesting, no excessive bullet points)
- Technical accuracy without jargon overload
- Hypothesis-driven presentation (state what you expect and why)

**Structure Guidelines**:
- Lead with context and problem statement
- Use simple section headers (## and ### only, no deeper nesting)
- Reserve bullet points for discrete facts, not narrative content
- Let ideas flow naturally from paragraph to paragraph
- Avoid heavy formatting (tables, nested lists, excessive code blocks)

**Content Characteristics**:
- Brief but complete: cover essential information without bloat
- Evidence-based: support claims with real metrics and observations
- Actionable: readers should understand both what and why
- Honest about tradeoffs: document caveats and limitations clearly

**Examples**:
- Good: "We faced a significant challenge with class imbalance in our assembled dataset. The laptop class dominated at 88% of all annotations while microwaves represented only 0.4%, creating a 225:1 imbalance ratio."
- Bad: "## Dataset Composition\n### Class Distribution Analysis\n- Laptop: 88%\n- Microwave: 0.4%\n- Imbalance ratio: 225:1"

See TRAINING_APPROACH.md for reference implementation of this style.

### Markdown Formatting Rules

**Typography Standards**:
- **No em-dashes**: Use single hyphen with spaces (` - `) instead of em-dash (`—`)
- **No arrow symbols in prose**: Use ASCII `->` instead of arrow characters (→, ⇒, etc.) in narrative text
- **Line breaks**: Use `<br>` tag or double-space at end of line for explicit breaks within paragraphs
- **Paragraph separation**: Use blank lines between paragraphs (standard markdown)
- **No emojis**: Use unicode characters instead of emojis for visual indicators

**Examples**:
- Good: `dataset - minimal contamination`
- Bad: `dataset—minimal contamination`
- Good: `A -> B -> C`
- Bad: `A → B → C` or `A ⇒ B ⇒ C`

**Unicode Indicators** (for training reports, progress displays, status indicators):
- **Trend Indicators**:
  - `↑` (U+2191) - Upward trend
  - `↓` (U+2193) - Downward trend
  - `↗` (U+2197) - Slight increase
  - `↘` (U+2198) - Slight decrease
  - `━` (U+2501) - Stable/flat
  - `⇑` (U+21D1) - Strong climb
  - `⇓` (U+21D3) - Strong drop
- **Status Indicators**:
  - `✓` (U+2713) - Check mark (success)
  - `✗` (U+2717) - X mark (failure)
  - `⚠` (U+26A0) - Warning
  - `►` (U+25BA) - Action/attention marker
  - `•` (U+2022) - Bullet point

### Markdown Alert Boxes

When warranted, use special styles in markdown documentation to highlight tips, warnings, examples, or critical actions:

```html
<div class="alert alert-block alert-info">
<b>Tip:</b> Use blue boxes (alert-info) for tips and notes.
</div>

<div class="alert alert-block alert-warning">
<b>Warning:</b> Use yellow boxes for warnings or important caveats.
</div>

<div class="alert alert-block alert-success">
<b>Success:</b> Use green boxes sparingly for confirmations or related links.
</div>

<div class="alert alert-block alert-danger">
<b>Critical:</b> Use red boxes only for actions that might cause data loss or major issues.
</div>
```

## Workflow Guidelines

1. Always check CHECKLIST.md before starting a new phase
2. Ask user for clarification when encountering decision points above
3. Document key decisions and rationales in notebooks
4. Save intermediate results and checkpoints to appropriate directories
5. Update journal after completing major tasks

## Project Structure Standards

**Follow cookiecutter-data-science structure**:
- `data/raw/` - Original immutable dataset (homeobjects-3k)
- `data/interim/` - Filtered electronics dataset with annotations
- `data/processed/` - Final train/val/test splits in YOLO format
- `models/` - Trained model checkpoints (.pt files)
- `reports/` - Performance report (generated from REPORT_TEMPLATE.md)
- `reports/figures/` - Training curves, confusion matrices, visualizations
- `notebooks/` - Jupytext .py notebooks (percent format)
- `references/` - Dataset documentation, class definitions

## Training Requirements

**Ultralytics Configuration**:
- **MANDATORY**: Use project-local Ultralytics settings (.config/Ultralytics/settings.json)
- **Setup**: Source `.env` file before running any YOLO commands: `source .env`
- The `.env` file sets `YOLO_CONFIG_DIR` to point to `.config/` directory
- Project-local settings configured with:
  - weights_dir: `models/pretrained/` (absolute path)
  - datasets_dir: `datasets/` (project-relative)
  - runs_dir: `runs/` (project-relative)
- Verify: `source .env && conda run --name hk_yolo python -c "from ultralytics import settings; print(settings.file)"`
- .gitignore: `/*.pt` pattern prevents accidental commits of auto-downloaded models in project root

**Log Cleanup Between Runs**:
- **MANDATORY**: Clean test/temporary logs before launching new training runs
- Remove old training logs (training-test-*.log, epoch-progress.log, etc.)
- Keep only production logs (dataset-sourcing.log, dataset-harmonization.log, dataset-splitting.log, training-yolov8m-*.log)
- Update logs/README.md with current log inventory after cleanup
- Example cleanup command: `rm -f logs/training-test-*.log logs/epoch-progress.log`

**GPU Selection**: Always detect and use the best available GPU based on compute capability
- Check available GPUs before training
- Select GPU by compute characteristics (architecture, performance) not just memory
- Prefer newer GPU architectures for better performance
- Display GPU information (name, memory, CUDA version, compute capability)
- Set CUDA device explicitly in training scripts
- **CRITICAL**: Use CUDA_VISIBLE_DEVICES environment variable to force specific GPU isolation
- Example: Higher compute capability GPUs (12.0) outperform lower ones (8.9) despite similar memory
- Verify actual GPU usage with nvidia-smi after launch (not just script output)

**Performance Report**: Generate comprehensive report after training
- Use `.claude/REPORT_TEMPLATE.md` as template
- Save final report to `reports/performance-report.md`
- Include all visualizations in `reports/figures/`
- Generate comparison tables and metrics
- Document model artifacts locations
- **IMPORTANT**: Document hardware used (GPU model, memory, driver versions)
- **IMPORTANT**: Record total training time and average epoch time
