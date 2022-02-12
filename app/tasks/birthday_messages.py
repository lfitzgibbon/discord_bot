import pytz
import random
from datetime import datetime

from app import BOT_TIMEZONE


# Each entry here is a message and a multiplicative conversion to apply the user's age to
# generate an interesting fact. The message should be an unformatted string that leaves
# a space for the eventual conversion to be inserted
# These numbers are just pulled from Google searches, so there might be some fake news here
MESSAGES = [
    {"conv": 0.5, "msg": "They have grown ~{} feet of hair in their lifetime! ✂"},
    {"conv": 0.01944, "msg": "They have grown ~{} meters of fingernails in their lifetime! 💅"},
    {"conv": 71, "msg": "~{} people have been attacked by sharks in their lifetime! 🦈"},
    {"conv": 46, "msg": "They have eaten ~{} slices of pizza in their lifetime! 🍕"},
    {"conv": 4.5, "msg": "Americans have eaten ~{} billion tacos in their lifetime! 🌮"},
    {"conv": 1.4, "msg": "Lightning has stuck ~{} billion times in their lifetime! ⚡"},
    {"conv": 5.110, "msg": "They have farted ~{} thousand times in their lifetime! 💨"},
    #{"conv": 0, "msg": ""},
    #{"conv": 0, "msg": ""},
    #{"conv": 0, "msg": ""},
    #{"conv": 0, "msg": ""},
    #{"conv": 0, "msg": ""},
    #{"conv": 0, "msg": ""},
    #{"conv": 0, "msg": ""},
    #{"conv": 0, "msg": ""},
]

def make_ordinal(n: int) -> str:
    '''
    Source: https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    Convert an integer into its ordinal representation
    '''
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def construct_birthday_message(user: str, birth_year: int) -> str:
    msg_choice = random.choice(MESSAGES)

    now = datetime.now(tz=pytz.timezone(BOT_TIMEZONE))

    age = now.year - birth_year
    ordinal_age = make_ordinal(age)
    fun_fact = msg_choice["msg"].format(msg_choice["conv"] * age)
    
    return f"Happy {ordinal_age} birthday {user} 🥳 \n" + fun_fact
