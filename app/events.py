from discord.ext.commands.context import Context

from app import BOT

@BOT.event
async def on_command_error(ctx: Context, error):
    await ctx.send(f"Error processing command: '{error}'")
