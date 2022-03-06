import os
import sys
import logging

from app import BOT
from app.database import db_connect
from app.tasks.tasks import start_tasks


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Establish a connection to the database
    db_connect()

    token = os.getenv("LILYBOT_TOKEN")
    if not token:
        logging.error("Could not find client token")
        sys.exit(1)

    logging.info("Starting up LilyBot")

    try:
        start_tasks()
        BOT.run(token)
    except BaseException as err:
        logging.exception(err)
