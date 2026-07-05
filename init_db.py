from database import get_db_connection


def initialize_database():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code VARCHAR(10) UNIQUE,
            original_url VARCHAR(255) NOT NULL,
            status VARCHAR(20)
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully!")


if __name__ == "__main__":
    initialize_database()