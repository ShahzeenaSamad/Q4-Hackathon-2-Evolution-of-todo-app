# Alembic Migrations

Database migrations for Phase 3 AI-Powered Todo Chatbot.

## Configuration

The database URL is loaded from the `.env` file via `alembic/env.py`.
No need to hardcode it in `alembic.ini`.

## Creating Migrations

### Auto-generate from models

```bash
# Auto-generate migration based on model changes
alembic revision --autogenerate -m "Description of changes"
```

### Manual migration

```bash
# Create a blank migration template
alembic revision -m "Description of migration"
```

## Running Migrations

### Upgrade to latest

```bash
alembic upgrade head
```

### Upgrade to specific version

```bash
alembic upgrade <revision_id>
```

### Downgrade one step

```bash
alembic downgrade -1
```

### Downgrade to base (no tables)

```bash
alembic downgrade base
```

## Viewing History

```bash
# Show all migration versions
alembic history

# Show current version
alembic current
```

## Phase 3 Migration Files

- `003_add_conversations.py` - Add Conversation and Message tables for chat functionality

## Notes

- Always ensure `.env` file exists before running migrations
- Test migrations in development before production
- Keep migration files in version control
