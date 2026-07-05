import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


DATABASE_PATH = os.path.join(BASE_DIR, "database", "urls.db")


REDIS_BROKER_URL = "redis://localhost:6379/0"


REDIS_RESULT_BACKEND = "redis://localhost:6379/0"