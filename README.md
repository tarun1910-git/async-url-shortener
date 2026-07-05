# Async URL Shortener with Redis

A Flask-based URL Shortener that demonstrates asynchronous background processing using Redis and Celery.

## Features

- Generate unique short URLs
- Validate URLs using Marshmallow
- Store data in SQLite
- Asynchronous background processing using Celery
- Redis as the message broker
- URL redirection
- URL status API

## Tech Stack

- Python
- Flask
- SQLite
- Redis
- Celery
- Marshmallow

---

## Project Structure

```
async-url-shortener/
│
├── app.py
├── celery_worker.py
├── config.py
├── database.py
├── init_db.py
├── schemas.py
├── tasks.py
├── requirements.txt
├── routes/
│   └── url_routes.py
└── database/
    └── urls.db
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd async-url-shortener
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Start Redis

Make sure Redis Server is running on

```
localhost:6379
```

---

## Initialize Database

```bash
python init_db.py
```

---

## Start Celery Worker

```bash
celery -A celery_worker worker --pool=solo --loglevel=info
```

---

## Start Flask

```bash
python app.py
```

Application runs on

```
http://127.0.0.1:5000
```

---

## API Endpoints

### Shorten URL

POST

```
/shorten
```

Request

```json
{
    "url":"https://google.com"
}
```

Response

```json
{
    "message":"Short URL request accepted.",
    "short_code":"AbC123",
    "original_url":"https://google.com",
    "status":"PENDING"
}
```

---

### Get URL Status

GET

```
/url/<short_code>
```

Response

```json
{
    "short_code":"AbC123",
    "original_url":"https://google.com",
    "status":"ACTIVE"
}
```

---

### Redirect

GET

```
/<short_code>
```

Redirects to the original URL.
