''' Birthday Repository '''
import pytz
from typing import List
from datetime import datetime

from app import BOT_TIMEZONE
from app.database.models.birthday import Birthday
from app.util.query import remove_none_values


class BirthdayRepository:
    ''' Methods to retrieve birthday data '''

    def find(self,
        birth_month: int = None,
        birth_day: int = None,
        server_id: int = None,
        channel_id: int = None
    ) -> List[Birthday]:
        ''' Get a list of all birthdays occuring on the given day '''
        sanitized_kwargs = remove_none_values({
            "birth_month": birth_month,
            "birth_day": birth_day,
            "server_id": server_id,
            "channel_id": channel_id
        })

        days_bdays = Birthday.objects(**sanitized_kwargs)
        return list(days_bdays)

    def find_today(self) -> List[Birthday]:
        ''' Get a list of all birthdays occuring on the current day '''
        today = datetime.now(tz=pytz.timezone(BOT_TIMEZONE))

        return self.find(
            birth_month=today.month,
            birth_day=today.day
        )

    def register(self, 
        user: str,
        birthday: datetime,
        server_id: int,
        channel_id: int = None
    ) -> int:
        '''
        Register the given user's birthday
        If the given user isn't yet registered to this server, create a new entry
        If they are already registered, update the existing entry
        Returns the number of objects updated (should be 1)
        '''
        return Birthday.objects(
            server_id=server_id,
            user=user
        ).update_one(
            upsert=True,
            set__user=user,
            set__birth_year=birthday.year,
            set__birth_month=birthday.month,
            set__birth_day=birthday.day,
            set__server_id=server_id,
            set__channel_id=channel_id
        )

    def delete_user_bday(self, server_id: int, user: str) -> int:
        ''' Delete the birthday associated with the given user from the given server '''
        # TODO: implement
        pass
