from app import models, schemas
from datetime import datetime
from databases import cache


def get_receipt(receipt_id: int):
    if cache.check_key(receipt_id) == {}:
        result = models.Receipt.filter(models.Receipt.id == receipt_id).first()
        if result is None:
            return result
        else:
            cache.add_key(
                receipt_id,
                result.rec_num,
                result.reg_num,
                result.total,
                result.date,
            )
    else:
        pass
    print('This is get recipt func!')
    return cache.check_key(receipt_id)


def delete_receipt(receipt_id: int):
    db_user = models.Receipt.filter(models.Receipt.id == receipt_id).first()
    if db_user is None:
        return None
    else:
        db_user.delete_instance()
        print('This is delete func!')
        return db_user


def get_receipt_by_recnum(rec_num: str):
    print('This is get by recnum func!')
    return models.Receipt.filter(models.Receipt.rec_num == rec_num).first()


def get_receipts(skip: int = 0, limit: int = 100):
    return list(models.Receipt.select().offset(skip).limit(limit))


def create_receipt(receipt: schemas.ReceiptCreate):
    db_receipt = models.Receipt(
        rec_num=receipt.rec_num,
        reg_num=receipt.reg_num,
        total=receipt.total,
        date=receipt.date
    )
    db_receipt.save()
    print('This is create receipt func!')
    return db_receipt


