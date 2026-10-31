import asyncio
import os
from sqlalchemy.engine import make_url

import asyncpg


async def main():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        url = make_url(db_url)
        user = url.username
        password = url.password
        database = url.database
        host = url.host
        port = url.port or 5432
    else:
        user = os.environ.get("POSTGRES_USER", "agentsec")
        password = os.environ.get("POSTGRES_PASSWORD", "agentsec123")
        database = os.environ.get("POSTGRES_DB", "agentsecdb")
        host = os.environ.get("POSTGRES_HOST", "localhost")
        port = int(os.environ.get("POSTGRES_PORT", "5432"))

    try:
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
        )
        rows = await conn.fetch("select tablename from pg_tables where schemaname = 'public';")
        print("tables:", [r[0] for r in rows])
        await conn.close()
    except (asyncpg.PostgresError, OSError) as e:
        print(f"error connecting to {host}:{port}/{database}: {e}")
        raise SystemExit(1) from e


if __name__ == "__main__":
    asyncio.run(main())
