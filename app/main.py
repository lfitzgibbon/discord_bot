import os
import sys
import logging

from mongoengine import connect

from app import BOT
from app.tasks.tasks import start_tasks


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # TODO: this should be in the database module and have better configurability
    connect("lilybot")

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
