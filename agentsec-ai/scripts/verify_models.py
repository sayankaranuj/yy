"""Verify SQLAlchemy models by compiling CREATE TABLE DDL (Postgres dialect).

This does not require a running database; it only ensures the SQLAlchemy
metadata and types compile for PostgreSQL.
"""

from __future__ import annotations

from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from backend.models import base as models_base
import backend.models  # noqa: F401  # ensure all models are imported and registered


def main() -> None:
    md = models_base.Base.metadata
    tables = list(md.sorted_tables)
    if not tables:
        print("No tables found in metadata.")
        return
    for t in tables:
        ddl = CreateTable(t).compile(dialect=postgresql.dialect())
        print(ddl)


if __name__ == "__main__":
    main()
