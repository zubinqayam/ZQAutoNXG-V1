from __future__ import annotations

import os
from collections.abc import Mapping
from urllib.parse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


LOCAL_DATABASE_URL = "sqlite:///./data/zqautonxg.db"
VERCEL_DATABASE_URL = "sqlite:////tmp/zqautonxg.db"
LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _normalise_postgres_url(url: str) -> str:
    """Return SQLAlchemy's supported PostgreSQL URL spelling."""
    if url.startswith("postgres://"):
        return f"postgresql://{url.removeprefix('postgres://')}"
    return url


def _uses_loopback_host(url: str) -> bool:
    """Return whether a network database URL points back to this process."""
    try:
        return urlparse(url).hostname in LOOPBACK_HOSTS
    except ValueError:
        return False


def resolve_database_url(environ: Mapping[str, str] | None = None) -> str:
    """Resolve a database URL that is valid for the active runtime.

    Vercel functions cannot reach services addressed as localhost and only
    expose a writable filesystem under /tmp. A loopback URL is therefore
    treated as a local-development placeholder, while a remote database URL
    remains authoritative.
    """
    environment = os.environ if environ is None else environ
    configured_url = _normalise_postgres_url(
        environment.get("DATABASE_URL", "").strip()
    )

    if environment.get("VERCEL") and (
        not configured_url or _uses_loopback_host(configured_url)
    ):
        return VERCEL_DATABASE_URL

    return configured_url or LOCAL_DATABASE_URL


SQLALCHEMY_DATABASE_URL = resolve_database_url()

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

