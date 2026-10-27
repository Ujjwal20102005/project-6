"""Minimal versioned SQL migration runner: applies migrations/*.sql in order."""
import pathlib

from sqlalchemy import text

from src.core.database import engine

MIGRATIONS = pathlib.Path(__file__).resolve().parents[2] / "migrations"


def run_migrations() -> list:
    applied = []
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS schema_version (name TEXT PRIMARY KEY)"))
        done = {r[0] for r in conn.execute(text("SELECT name FROM schema_version"))}
        for f in sorted(MIGRATIONS.glob("*.sql")):
            if f.name in done:
                continue
            for stmt in f.read_text().split(";"):
                if stmt.strip():
                    conn.execute(text(stmt))
            conn.execute(text("INSERT INTO schema_version VALUES (:n)"), {"n": f.name})
            applied.append(f.name)
    return applied


if __name__ == "__main__":
    print("Applied:", run_migrations())
