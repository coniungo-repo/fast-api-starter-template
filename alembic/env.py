import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from src.core.config import settings
from src.database.base import Base
from src.modules.users.domain.models import User

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Helper function to execute migrations within the context runner."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an AsyncEngine."""
    # Retrieve the database URL specified by your app configuration settings
    url = config.get_main_option("sqlalchemy.url")

    # Initialize the correct Asynchronous Engine explicitly
    connectable = create_async_engine(
        url=str(url),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Instruct SQLAlchemy to bridge execution synchronously to Alembic
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Run the online migration loop inside an event runner loop
    asyncio.run(run_migrations_online())
