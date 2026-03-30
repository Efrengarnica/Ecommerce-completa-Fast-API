import asyncio
from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

from database import engine

# Alembic Config object
config = context.config


#Faltaria importar los modelos
from models.producto import *

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de tus modelos SQLModel para autogenerate
target_metadata = SQLModel.metadata


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
    """Ejecuta las migraciones usando una conexión síncrona adaptada."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with AsyncEngine."""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# Comandos para poder ejecutar las migraciones:
# docker exec -it contenedor_ecommerce_api alembic revision --autogenerate -m "Tabla Producto"