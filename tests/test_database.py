from db.database import DATABASE_PATH, get_connection


def test_database_has_expected_tables_and_imported_rows() -> None:
    with get_connection() as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        film_count = connection.execute(
            "SELECT COUNT(*) AS count FROM films"
        ).fetchone()["count"]
        average = connection.execute(
            "SELECT ROUND(AVG(value), 1) AS average FROM ratings"
        ).fetchone()["average"]

    assert DATABASE_PATH.exists()
    expected_tables = {
        "films", "genres", "film_genres", "users", "ratings", "statuses"
    }
    assert expected_tables <= tables
    assert film_count == 1
    assert average == 9.0


def test_foreign_keys_are_enabled() -> None:
    with get_connection() as connection:
        enabled = connection.execute("PRAGMA foreign_keys").fetchone()[0]

    assert enabled == 1
