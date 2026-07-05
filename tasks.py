from celery_worker import celery
from database import get_db_connection


@celery.task
def process_url(message):

    url_id = message["id"]
    url = message["url"]

    if url.startswith("http://") or url.startswith("https://"):
        status = "ACTIVE"
    else:
        status = "INVALID"

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE urls
        SET status = ?
        WHERE id = ?
        """,
        (status, url_id)
    )

    connection.commit()
    connection.close()