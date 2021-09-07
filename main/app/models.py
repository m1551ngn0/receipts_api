from peewee import CharField, Model, DateTimeField

from databases import database


class Receipt(Model):
    receipt_num = CharField(unique=True)
    registration_num = CharField()
    total = CharField()
    created_at = DateTimeField()

    class Meta:
        database = database.db
