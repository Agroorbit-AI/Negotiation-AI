from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic Config
config = context.config

# Force Alembic to use DATABASE_URL from environment (Render)
database_url = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", database_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models
from app.db.base import Base
target_metadata = Base.metadata


def run_migrations_offline():
    url = database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": database_url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
