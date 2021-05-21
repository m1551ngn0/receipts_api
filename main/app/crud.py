from app import models, schemas
from datetime import datetime
from databases import cache

now = datetime.now()
older = datetime(2000, 1, 1)


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
                result.date,
                result.total
            )
    else:
        pass
    return cache.check_key(receipt_id)


def delete_receipt(receipt_id: int):
    db_user = models.Receipt.filter(models.Receipt.id == receipt_id).first()
    if db_user is None:
        return None
    else:
        db_user.delete_instance()
        return db_user


def get_receipt_by_email(rec_num: str):
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
    return db_receipt


def before_date_filter(rec_num: str):
    return models.Receipt.select().where(models.Receipt.rec_num == rec_num)


"""def reg_num_filter(reg_num: str):
    return models.Receipt.filter(models.Receipt.reg_num == reg_num).first()"""
