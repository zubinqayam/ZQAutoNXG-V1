from zqautonxg.database import (
    LOCAL_DATABASE_URL,
    VERCEL_DATABASE_URL,
    resolve_database_url,
)


def test_local_runtime_keeps_the_existing_sqlite_default():
    assert resolve_database_url({}) == LOCAL_DATABASE_URL


def test_vercel_runtime_uses_its_writable_filesystem_by_default():
    assert resolve_database_url({"VERCEL": "1"}) == VERCEL_DATABASE_URL


def test_vercel_runtime_rejects_a_loopback_postgres_placeholder():
    environment = {
        "VERCEL": "1",
        "DATABASE_URL": "postgresql://user:password@localhost:5432/app",
    }

    assert resolve_database_url(environment) == VERCEL_DATABASE_URL


def test_vercel_runtime_preserves_a_remote_database():
    database_url = "postgresql://user:password@db.example.com:5432/app"

    assert (
        resolve_database_url({"VERCEL": "1", "DATABASE_URL": database_url})
        == database_url
    )


def test_legacy_postgres_scheme_is_normalised_for_sqlalchemy():
    assert (
        resolve_database_url(
            {"DATABASE_URL": "postgres://user:password@db.example.com:5432/app"}
        )
        == "postgresql://user:password@db.example.com:5432/app"
    )

