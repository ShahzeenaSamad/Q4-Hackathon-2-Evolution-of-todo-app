---
description: "Show help for Spec-Kit Plus commands"
---

# Spec-Kit Plus Help Command

## Usage
```
/sp.help [command-name]
```

## Description
Displays help information for Spec-Kit Plus commands.

## Options

### Show All Commands
```
/sp.help
```
Lists all available Spec-Kit Plus commands with brief descriptions.

### Show Specific Command Help
```
/sp.help <command-name>
```
Shows detailed help for a specific command.

Example:
```
/sp.help spec
```
Shows detailed help for `/sp.spec` command.

## Available Commands

### Constitution & Governance
- **/sp.constitution** - Manage project constitution
- **/sp.adr** - Document architectural decisions

### Specification & Planning
- **/sp.spec** - Create feature specifications
- **/sp.plan** - Create implementation plans
- **/sp.tasks** - Generate task breakdowns

### Project Management
- **/sp.init** - Initialize Spec-Kit Plus
- **/sp.status** - Show project status
- **/sp.help** - Show this help message

## Quick Reference

### Spec-Driven Development Workflow
```
1. /sp.spec <feature>        # Create specification
2. /sp.plan <feature>        # Create implementation plan
3. /sp.tasks <feature>       # Generate tasks
4. Implement via Claude Code
5. /sp.adr <decision>        # Document architectural decisions
```

### Constitution Management
```
/sp.constitution              # View constitution
/sp.constitution --amend      # Propose amendment
```

## Command Categories

### For Project Setup
- `/sp.init` - One-time setup
- `/sp.constitution` - Set governance

### For Feature Development
- `/sp.spec` - Define features
- `/sp.plan` - Plan implementation
- `/sp.tasks` - Break down work

### For Documentation
- `/sp.adr` - Document decisions
- `/sp.phr` - View prompt history

## Getting Started

### New Project Setup
```bash
# 1. Initialize Spec-Kit Plus
/sp.init --full

# 2. Customize constitution
nano CONSTITUTION.md

# 3. Create project overview
/sp.spec overview "My project overview"

# 4. Start first feature
/sp.spec my-first-feature
```

### Feature Development
```bash
# 1. Create specification
/sp.spec feature-name

# 2. Create implementation plan
/sp.plan feature-name

# 3. Generate tasks
/sp.tasks feature-name

# 4. Implement with Claude Code
@specs/features/feature-name/spec.md implement this feature

# 5. Document decisions
/sp.adr decision-title
```

## Examples

### Get Help for Specific Command
```bash
/sp.help spec
```
Shows detailed help for `/sp.spec` command.

### List All Commands
```bash
/sp.help
```
Shows all available commands.

## Templates Reference

### Specification Templates
- `spec-template.md` - Feature specification
- `plan-template.md` - Implementation plan
- `tasks-template.md` - Task breakdown
- `adr-template.md` - Architecture decision
- `phr-template.prompt.md` - Prompt history

### File Locations
- Templates: `.specify/templates/`
- Commands: `.specify/templates/commands/`
- Specs: `specs/`
- History: `history/`

## Constitution Compliance

All Spec-Kit Plus commands follow these principles:

### I. Spec-Driven Development
- No implementation without spec
- Specs referenced with @specs/ path
- Iterative refinement until correct

### II. AI as Implementation Engine
- Claude Code generates from specs
- No manual code writing
- Humans write specs, AI writes code

### III. Human as System Architect
- Humans design and decide
- AI implements and suggests
- Collaboration between human and AI

## Troubleshooting

### Command Not Found
If command doesn't appear:
1. Verify `.specify/templates/commands/` exists
2. Check command file has correct frontmatter
3. Run `/sp.init --force` to recreate

### Spec Not Found
If spec reference fails:
1. Check file exists: `ls specs/features/`
2. Verify path: `@specs/features/name/spec.md`
3. Create spec: `/sp.spec feature-name`

### Templates Missing
If templates not found:
1. Check `.specify/templates/` exists
2. Verify template files present
3. Run `/sp.init --force` to recreate

## See Also
- `/sp.constitution` - View governing principles
- `/sp.init` - Initialize Spec-Kit Plus
- `/sp.status` - Check project status
