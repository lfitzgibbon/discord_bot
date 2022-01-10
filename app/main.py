import os
import sys
import logging

from app import BOT


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    token = os.getenv("LILYBOT_TOKEN")
    if not token:
        logging.error("Could not find client token")
        sys.exit(1)

    logging.info("Starting up LilyBot")

    try:
        BOT.run(token)
    except BaseException as err:
        logging.exception(err)
