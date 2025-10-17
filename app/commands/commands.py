import math
import random
from datetime import datetime
from discord.ext.commands.context import Context

from app import BOT
from app.commands.metadata import COMMAND_INFO, build_command_help_msg
from app.database.repositories.birthday import BirthdayRepository


# Remove the default help command, so that we can register our own
BOT.remove_command("help")

@BOT.listen()
async def on_message(message):
    """Special message handling that is not covered by prefixed commands"""
    if message.author == BOT.user:
        return

    # If the message only has the word "sneeze" in it, determine if the person is worthy of being blessed
    unique_words = set(message.content.lower().split())
    if unique_words == {"sneeze"} and random.randint(1, 20) == 20:
        await message.channel.send('bless you 🙏')


@BOT.command("help")
async def help(ctx: Context, command: str = None) -> None:
    if metadata := COMMAND_INFO.get(command):
        # If the user wanted information regarding a specific command, just return that info
        help_msg = build_command_help_msg(command, metadata)
    else:
        help_msg = "Welcome to LilyBOT!\n\n"
        help_msg += "Available commands:"

        for command, metadata in COMMAND_INFO.items():
            help_msg += build_command_help_msg(command, metadata)
    
    await ctx.channel.send(f"```\n{help_msg}\n```")

@BOT.command(name="birthday")
async def register_birthday(ctx: Context, birthday: str, *user: str) -> None:
    ''' Register the given birthday to either the current or given user '''
    # Validate that the user has given a birthday, and that the birthday is valid
    try:
        parsed_birthday = datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        await ctx.send("Incorrect date format, use 'YYYY-mm-dd'.")
        return

    user = " ".join(user) if user else ctx.message.author.mention
    server_id = ctx.guild.id
    channel_id = ctx.channel.id

    bday_repo = BirthdayRepository()
    bday_repo.register(user, parsed_birthday, server_id, channel_id)

    # TODO: it'd be cute if it also returned the number of days until next bday
    # Leaps years might make that weird though
    await ctx.channel.send("Birthday has been successfully registered!")

@BOT.command(name="choose")
async def choose_idea(ctx: Context, after: str = None) -> None:
    ''' Choses a random option from those provided in the current channel '''
    choice_prefix = "idea"

    # Attempt to parse the date that was given, if applicable
    if after:
        try:
            after = datetime.strptime(after, "%Y-%m-%d")
        except ValueError:
            await ctx.channel.send("Incorrect date format, use 'YYYY-mm-dd'.")
            return

    # Retrieve the message history, only saving those that start with the magic phrase
    # Change the limit away from "None" here if it starts to be too slow
    choices = []
    fewest_picks = math.inf
    async for message in ctx.channel.history(limit=None, after=after):
        if message.content.lower().startswith(choice_prefix):
            choices.append(message)
        
            # Check to see if this has fewer reactions than any message thus far
            num_rxns = len(message.reactions)
            if num_rxns < fewest_picks:
                fewest_picks = num_rxns

    if not choices:
        if after:
            await ctx.channel.send("Couldn't find any suggestions in this channel after the given time!")
        else:
            await ctx.channel.send("You haven't suggested anything in this channel yet!")
        return

    # Select a choice from the subset that have the fewest number of reactions
    selection = random.choice([x for x in choices if len(x.reactions) == fewest_picks])

    # Construct and send the message
    response = "As suggested by {0.author} at {0.created_at}:\n\n".format(selection)

    # Determine what the content of the message looks like
    # If there are no embeds, just include the raw text of the original message
    if not selection.embeds:
        embedded_obj = None
        response += '"{0.content}"\n\n'.format(selection)
    else:
        embedded_obj = selection.embeds[0]

    response += "This has been chosen at least {} time(s) before.".format(fewest_picks)
    await ctx.channel.send(content=response, embed=embedded_obj)

    # Since each post can only have one type of each reaction, have a list to cycle through
    # If the post is at max reactions, don't bother
    if fewest_picks == 20:
        return

    emoji_selection = [
        "🦞", "🐙", "🐥", "🦗", "🐬", "🐦", "🦀", "🐤", "🐛", "🐟",
        "🦜", "🐠", "🐣", "🐍", "🐋", "❤", "🧡", "💛", "💚", "💙"
    ]

    await selection.add_reaction(emoji_selection[fewest_picks])
