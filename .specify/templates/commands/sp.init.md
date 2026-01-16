---
description: "Initialize Spec-Kit Plus for a new project"
---

# Spec-Kit Plus Initialization Command

## Usage
```
/sp.init [options]
```

## Description
Initializes Spec-Kit Plus in your project, creating the necessary folder structure and templates.

## Options
- `--full` - Create complete structure with all templates
- `--minimal` - Create minimal structure (constitution only)
- `--force` - Reinitialize even if already initialized

## What Gets Created

### Directory Structure
```
project-root/
├── .specify/
│   ├── memory/
│   │   └── constitution.md       # Project constitution
│   ├── templates/
│   │   ├── spec-template.md      # Feature spec template
│   │   ├── plan-template.md      # Implementation plan template
│   │   ├── tasks-template.md     # Task breakdown template
│   │   ├── adr-template.md       # Architecture decision record template
│   │   ├── phr-template.prompt.md # Prompt history record template
│   │   └── commands/             # Slash command definitions
│   │       ├── sp.spec.md
│   │       ├── sp.plan.md
│   │       ├── sp.tasks.md
│   │       ├── sp.adr.md
│   │       └── sp.constitution.md
│   ├── skills/                   # Reusable Agent Skills (optional)
│   └── subagents/                # Reusable Subagents (optional)
├── specs/
│   ├── overview.md               # Project overview
│   ├── features/                 # Feature specifications
│   ├── api/                      # API specifications
│   ├── database/                 # Database schemas
│   └── ui/                       # UI component specs
├── history/
│   ├── prompts/                  # Prompt history records
│   └── adr/                      # Architecture decision records
├── CONSTITUTION.md               # Root constitution (copy)
└── CLAUDE.md                     # Claude Code instructions
```

## Constitution Setup

When run, `/sp.init` will:
1. Create `CONSTITUTION.md` in root
2. Copy to `.specify/memory/constitution.md`
3. Create basic constitution with:
   - Project name and vision
   - Core principles
   - Development standards
   - AI governance rules

## Project Configuration

Creates `.specify/config.yaml`:
```yaml
name: your-project-name
version: "1.0"

structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui

phases:
  - name: phase1
    features: []
  - name: phase2
    features: []
```

## Templates

All templates are created from SpecKit Plus defaults:
- Feature specifications with user stories
- Implementation plans with technical context
- Task breakdowns with parallel opportunities
- ADRs for architectural decisions
- PHRs for prompt history

## Example Usage

### Initialize New Project
```
/sp.init
```
Creates basic Spec-Kit Plus structure.

### Full Initialization
```
/sp.init --full
```
Creates complete structure with all templates and example files.

### Force Reinitialize
```
/sp.init --force
```
Overwrites existing structure (use with caution).

## Post-Initialization Steps

1. **Customize Constitution**
   Edit `CONSTITUTION.md` with your project details:
   ```bash
   nano CONSTITUTION.md
   ```

2. **Create Project Overview**
   ```bash
   /sp.spec overview "Project overview and goals"
   ```

3. **Create First Feature Spec**
   ```bash
   /sp.spec my-first-feature
   ```

4. **Create Implementation Plan**
   ```bash
   /sp.plan my-first-feature
   ```

5. **Generate Tasks**
   ```bash
   /sp.tasks my-first-feature
   ```

## Verification

After initialization, verify:
```bash
# Check structure exists
ls -la .specify/

# Check templates
ls -la .specify/templates/

# Check commands available
/sp.help

# Check constitution
cat CONSTITUTION.md
```

## Troubleshooting

### Commands Not Showing
If `/sp.*` commands don't appear:
1. Verify `.specify/templates/commands/` exists
2. Check command files have correct frontmatter
3. Reload Claude Code

### Constitution Missing
If `CONSTITUTION.md` missing:
1. Check `.specify/memory/constitution.md` exists
2. Copy manually: `cp .specify/memory/constitution.md CONSTITUTION.md`
3. Or run `/sp.init --force`

### Templates Not Found
If templates are missing:
1. Verify `.specify/templates/` folder exists
2. Check template files are present
3. Run `/sp.init --force` to recreate

## See Also
- `/sp.constitution` - View/amend constitution
- `/sp.spec` - Create feature specification
- `/sp.help` - Show all available commands
