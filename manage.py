from typing import Any

import click
import uvicorn

from alembic.config import Config
from app.base.config import settings


@click.group()
def cli() -> None:
    """
    Simple CLI For Managing Sanic app
    """
    pass


@cli.command(help="Show current revision")
def current() -> None:
    """
    Show current revision
    """
    from alembic.command import current

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("db_url", str(settings.db_url))

    current(alembic_cfg)


@cli.command(help="Show history revision")
def migrationshistory() -> None:
    """
    Show history revision
    """
    from alembic.command import history

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)

    history(alembic_cfg)


@cli.command(help="Auto make migrations")
@click.option("-m", help="Migration message")
def makemigrations(m: str) -> None:
    """
    Auto make migrations
    """
    from alembic.command import revision

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("db_url", str(settings.db_url))

    revision_kwargs: dict[str, Any] = {"autogenerate": True}
    if m is not None:
        revision_kwargs["message"] = m
    revision(alembic_cfg, **revision_kwargs)


@cli.command(help="apply migrations")
@click.argument("revision", default="head")
def migrate(revision: str) -> None:
    """
    apply migrations
    """
    from alembic.command import upgrade

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("db_url", str(settings.db_url))

    upgrade(alembic_cfg, revision)


@cli.command(help="Downgrade")
@click.argument("revision", default="1")
def downgrade(revision: str) -> None:
    """
    apply migrations
    """
    from alembic.command import downgrade

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("db_url", str(settings.db_url))

    downgrade(alembic_cfg, f"-{revision}")


@cli.command(help="stamp")
@click.argument("revision", default="head")
def stamp(revision: str) -> None:
    from alembic.command import stamp

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("db_url", str(settings.db_url))

    stamp(alembic_cfg, revision)


@cli.command(help="Run server")
@click.option("-h", "--host", default="0.0.0.0", help="Host")
@click.option("-p", "--port", type=click.INT, default=8000, help="Port")
def run_server(host: str, port: int) -> None:
    uvicorn.run("app.main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    cli()
