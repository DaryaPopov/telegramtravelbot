from peewee import *
import datetime
from config_data.config import BASE_DIR


db = SqliteDatabase(BASE_DIR/'database/requests.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    telegram_id = IntegerField(unique=True, null=False)


class Request(BaseModel):
    sent_date = DateTimeField(default=datetime.datetime.now)
    command = CharField(null=False)
    user_id = ForeignKeyField(User, null=False, related_name='telegram_ids')
    result = TextField()


with db:
    tables = [User, Request]
    if not all(table.table_exists() for table in tables):
        db.create_tables(tables)
    else:
        print('Таблицы уже существуют!')
