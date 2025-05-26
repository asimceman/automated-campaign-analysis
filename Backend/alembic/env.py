from alembic import context
from sqlalchemy import engine_from_config, pool
from app.models.ad import Ad
from app.settings import settings

target_metadata = Ad.metadata

config = context.config

def run_migrations_online() -> None:

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DB_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()