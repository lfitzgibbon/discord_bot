''' Birthday Model '''
from datetime import date
from mongoengine import Document, IntField, StringField
from mongoengine.errors import ValidationError

# Storing the birthday as three separate fields (year, month, day) allows us
# to easily query by just month/day (since a time range query is not practical
# to use here), and also allows us to create an index for these fields

class Birthday(Document):
    user = StringField(required=True)
    birth_day = IntField(required=True, min_value=1, max_value=31)
    birth_month = IntField(required=True, min_value=1, max_value=12)
    birth_year = IntField(required=True)
    server_id = IntField(required=True)
    channel_id = IntField()

    def validate(self, clean=True):
        super().validate(clean)

        # Make sure that the day/month/year combo is sensical
        try:
            date(self.birth_year, self.birth_month, self.birth_day)
        except ValueError:
            raise ValidationError("Combination of birth year, month, and day not a valid date.")
