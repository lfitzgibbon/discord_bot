from discord.ext import commands

# TODO: this should be configurable via command, and then all events in the server will use this TZ
# List of allowable timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
BOT_TIMEZONE = "America/Los_Angeles"

BOT = commands.Bot(command_prefix="!")

# These imports are unused here, but they function to register actions to the bot
# TODO: there is probably a more appropriate way to handle this
import app.commands.commands
import app.events