import os

from src.core import migrate
from src.core.database import engine


def test_migrations_idempotent(tmp_path):
    from sqlalchemy import create_engine
    migrate.engine = create_engine(f"sqlite:///{tmp_path}/m.db")
    try:
        assert migrate.run_migrations() == ["0001_init.sql"]
        assert migrate.run_migrations() == []
    finally:
        migrate.engine = engine
