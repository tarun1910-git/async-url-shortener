import pytest
from app import app
from database import get_db_connection
from tasks import process_url


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_urls.db"

    def get_test_db_connection():
        import sqlite3
        connection = sqlite3.connect(test_db)
        connection.row_factory = sqlite3.Row
        return connection

    # Replace the database connection used by the routes
    monkeypatch.setattr(
        "routes.url_routes.get_db_connection",
        get_test_db_connection
    )

    # Prevent Celery from contacting Redis
    monkeypatch.setattr(
        "routes.url_routes.process_url.delay",
        lambda message: None
    )

    # Create the test database
    connection = get_test_db_connection()
    connection.execute("""
        CREATE TABLE urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code VARCHAR(10) UNIQUE,
            original_url VARCHAR(255) NOT NULL,
            status VARCHAR(20)
        )
    """)
    connection.commit()
    connection.close()

    app.config["TESTING"] = True

    return app.test_client(), get_test_db_connection


def test_home_endpoint(client):
    test_client, _ = client

    response = test_client.get("/")

    assert response.status_code == 200
    assert b"Async URL Shortener API is Running!" in response.data


def test_shorten_valid_url(client):
    test_client, get_db = client

    response = test_client.post(
        "/shorten",
        json={"url": "https://example.com"}
    )

    assert response.status_code == 202

    data = response.get_json()

    assert data["original_url"] == "https://example.com"
    assert data["status"] == "PENDING"
    assert len(data["short_code"]) == 6

    connection = get_db()
    row = connection.execute(
        "SELECT * FROM urls WHERE short_code = ?",
        (data["short_code"],)
    ).fetchone()

    connection.close()

    assert row is not None
    assert row["status"] == "PENDING"


def test_shorten_invalid_url(client):
    test_client, _ = client

    response = test_client.post(
        "/shorten",
        json={"url": "not-a-valid-url"}
    )

    assert response.status_code == 400


def test_get_unknown_url(client):
    test_client, _ = client

    response = test_client.get("/url/unknown")

    assert response.status_code == 404


def test_redirect_unknown_url(client):
    test_client, _ = client

    response = test_client.get("/unknown")

    assert response.status_code == 404
