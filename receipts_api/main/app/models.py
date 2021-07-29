from peewee import CharField, Model, TimestampField

from databases import database


class Receipt(Model):
    rec_num = CharField(unique=True)
    reg_num = CharField()
    total = CharField()
    date = TimestampField()

    class Meta:
        database = database.db
