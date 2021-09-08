from app import models, schemas
from databases import cache


def get_receipt(receipt_id: int):
    check_result = cache.check_key(receipt_id)
    if check_result == {}:
        result = models.Receipt.filter(models.Receipt.id == receipt_id).first()
        if result is None:
            return None
        else:
            cache.add_key(
                receipt_id,
                result.receipt_num,
                result.registration_num,
                result.total,
                result.created_at,
            )
            return {
            'receipt_num': result.receipt_num,
            'registration_num': result.registration_num,
            'total': f'{result.total}',
            'created_at': f'{result.created_at}'        
            }
    else:
        return check_result
    


def delete_receipt(receipt_id: int):
    db_user = models.Receipt.filter(models.Receipt.id == receipt_id).first()
    if db_user is not None:
        db_user.delete_instance()
        cache.delete_key(receipt_id)
        return


def get_receipt_by_recnum(receipt_num: str):
    print('This is get by recnum func!')
    result = models.Receipt.filter(models.Receipt.receipt_num == receipt_num).first()
    if result is None:
        return
    else:
        return {
            'receipt_num': result.receipt_num,
            'registration_num': result.registration_num,
            'total': f'{result.total}',
            'created_at': f'{result.created_at}'        
            }


def get_receipt_by_regnum(registration_num: str):
    print('This is get by regnum func!')
    result = models.Receipt.filter(models.Receipt.registration_num == registration_num).first()
    if result is None:
        return
    else:
        return {
            'receipt_num': result.receipt_num,
            'registration_num': result.registration_num,
            'total': f'{result.total}',
            'created_at': f'{result.created_at}'        
            }


def get_receipts(skip: int = 0, limit: int = 100):
    return list(models.Receipt.select().offset(skip).limit(limit))


def create_receipt(receipt: schemas.ReceiptCreate):
    db_receipt = models.Receipt(
        receipt_num=receipt.receipt_num,
        registration_num=receipt.registration_num,
        total=receipt.total,
        created_at=receipt.created_at
    )
    db_receipt.save()
    print('This is create receipt func!')
    return db_receipt


