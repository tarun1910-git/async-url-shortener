from flask import Blueprint, request, redirect
from marshmallow import ValidationError
from schemas import URLSchema
from database import get_db_connection
from tasks import process_url
import random
import string


url_bp = Blueprint("url_bp", __name__)

schema = URLSchema()


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


@url_bp.route("/shorten", methods=["POST"])
def shorten_url():

    data = request.get_json()

    try:

        validated_data = schema.load(data)

        short_code = generate_short_code()

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO urls (short_code, original_url, status)
            VALUES (?, ?, ?)
            """,
            (
                short_code,
                validated_data["url"],
                "PENDING"
            )
        )

        connection.commit()

        url_id = cursor.lastrowid

        connection.close()

        message = {
            "id": url_id,
            "short_code": short_code,
            "url": validated_data["url"]
        }

        process_url.delay(message)

        return {
            "message": "Short URL request accepted.",
            "short_code": short_code,
            "original_url": validated_data["url"],
            "status": "PENDING"
        }, 202

    except ValidationError as err:

        return {
            "errors": err.messages
        }, 400


@url_bp.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT original_url
        FROM urls
        WHERE short_code = ?
        """,
        (short_code,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return redirect(result["original_url"])

    return {
        "message": "Short URL not found!"
    }, 404


@url_bp.route("/url/<short_code>", methods=["GET"])
def get_url(short_code):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT short_code, original_url, status
        FROM urls
        WHERE short_code = ?
        """,
        (short_code,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return {
            "short_code": result["short_code"],
            "original_url": result["original_url"],
            "status": result["status"]
        }, 200

    return {
        "message": "Short URL not found!"
    }, 404