from discord.ext import commands

BOT = commands.Bot(command_prefix="!")

# These imports are unused here, but they function to register actions to the bot
# TODO: there is probably a more appropriate way to handle this
import app.commands.commands
