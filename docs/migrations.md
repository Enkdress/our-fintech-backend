# Migrations

Managed by [Alembic](https://alembic.sqlalchemy.org/). Migration files live in `alembic/versions/`.

## Common commands

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Roll back one migration
uv run alembic downgrade -1

# Show current revision
uv run alembic current

# Show migration history
uv run alembic history

# Generate a new migration from model changes
uv run alembic revision --autogenerate -m "describe_the_change"
```

## After autogenerating a migration

Autogenerate produces a good starting point but requires two manual fixes before running:

1. **Add `import sqlmodel`** — autogenerate uses `sqlmodel.sql.sqltypes.AutoString()` but omits the import. Add it to the top of the file alongside the existing `import sqlalchemy as sa`.

2. **Review the diff** — autogenerate can miss things (e.g., column type changes, check constraints). Always read the generated file before applying it.

## SQLite constraint: NOT NULL columns

SQLite cannot add a `NOT NULL` column to an existing table via a plain `ALTER TABLE`. Use `op.batch_alter_table` with a `server_default` so Alembic rewrites the table via copy-and-move:

```python
def upgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(
            sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(),
                      nullable=False, server_default='')
        )
```

This applies to any schema change that involves constraints on an existing table (NOT NULL, UNIQUE, FK). Always use `op.batch_alter_table` for SQLite alterations.

## Migration history

| Revision | Description |
|---|---|
| `060311cebf17` | Initial schema — users, categories, transactions, budgets, debts |
| `789d18bb0463` | Add categories table (with system/user ownership) |
| `92c6f1e2d227` | Add `hashed_password` to users |
