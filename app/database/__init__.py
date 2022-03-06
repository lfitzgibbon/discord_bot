import os
import logging

from mongoengine import connect

def db_connect():
    connection_params = {
        "host": os.getenv("LILYBOT_DB_HOST", "mongodb://localhost:27017/?readPreference=primary"),
        "db": os.getenv("LILYBOT_DB_NAME", "lilybot"),
        "username": os.getenv("LILYBOT_DB_USER"),
        "password": os.getenv("LILYBOT_DB_PASS"),
    }

    connect(**connection_params)

    logging.info("Successfully connected to MongoDB.")
