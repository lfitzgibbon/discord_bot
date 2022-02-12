import asyncio
import logging
import discord
from discord.ext import tasks
from discord.utils import get

from app import BOT
from app.database.repositories.birthday import BirthdayRepository
from app.util.date import seconds_until_midnight
from app.tasks.birthday_messages import construct_birthday_message


@tasks.loop(hours=24)
async def send_birthday_alerts() -> None:
    ''' Send out birthday alerts at midnight '''
    # Sleep until it is time to send alerts
    # Add a bit of margin to account for float rounding errors - I've seen this go
    # off at 23:59:59.991 some days
    await asyncio.sleep(seconds_until_midnight() + 10)

    logging.info("Searching for birthdays.")

    # Gather all the birthdays
    bday_repo = BirthdayRepository()
    todays_bdays = bday_repo.find_today()

    # For each birthday, try to send the message to that server's #general channel
    # If that channel doesn't exist, send to the channel that the birthday message
    # was registered from (if saved)
    # If both fail, then nobody will know when it's their birthday :(
    logging.info(f"{len(todays_bdays)} birthday(s) found!")

    default_channel_name = "general"

    server_cache = {}
    for bday in todays_bdays:
        channel = server_cache.get(bday.server_id)

        if not channel:
            server = BOT.get_guild(bday.server_id)

            channel = (
                get(server.channels, name=default_channel_name, type=discord.ChannelType.text) or 
                get(server.channels, id=bday.channel_id, type=discord.ChannelType.text)
            )

            if channel is None:
                logging.error(f"Could not send birthday message to server ID {bday.server_id}.")
                continue

            server_cache[bday.server_id] = channel

        bday_msg = construct_birthday_message(bday.user, bday.birth_year)
        await channel.send(bday_msg)
    
    logging.info("Birthday messages sent!")

@send_birthday_alerts.before_loop
async def alert_setup() -> None:
    ''' Ensure that the bot is up and running before kicking off the alerts '''
    await BOT.wait_until_ready()

def start_tasks() -> None:
    ''' Kick off tasks '''
    send_birthday_alerts.start()
