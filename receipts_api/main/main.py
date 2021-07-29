from typing import List, Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from databases import database

database.db.connect()
database.db.create_tables([models.Receipt])
database.db.close()

app = FastAPI()

sleep_time = 10


async def reset_db_state():
    database.db._state._state.set(database.db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.post(
    "/receipts/",
    response_model=schemas.Receipt,
    dependencies=[Depends(get_db)]
)
def create_receipt(receipt: schemas.ReceiptCreate):
    db_receipt = crud.get_receipt_by_recnum(rec_num=receipt.rec_num)
    if db_receipt:
        raise HTTPException(
            status_code=400,
            detail="Чек с таким номером уже есть!"
        )
    print('This is main create func!')
    return crud.create_receipt(receipt=receipt)


@app.get(
    "/receipts/"
)
def read_receipts(skip: int = 0, limit: int = 100):
    receipts = crud.get_receipts(skip=skip, limit=limit)
    json_receipts = jsonable_encoder(receipts)
    return JSONResponse(content=json_receipts)


@app.get(
    "/receipts/{receipt_id}",
)
def read_receipt(receipt_id: int):
    db_receipt = crud.get_receipt(receipt_id=receipt_id)
    if db_receipt is None:
        raise HTTPException(
            status_code=404,
            detail="Чек с таким id не найден!"
        )
    json_db_receipt = jsonable_encoder(db_receipt)
    print('This is main read func!')
    return JSONResponse(content=json_db_receipt)


@app.delete(
    "/receipts/{receipt_id}",
    response_model=schemas.Receipt,
    dependencies=[Depends(get_db)]
)
def delete_receipt(receipt_id: int):
    check_none = crud.get_receipt(receipt_id=receipt_id)
    if check_none is None:
        raise HTTPException(
            status_code=404,
            detail="Чек с таким id не найден!"
        )
    print('This is main delete func!')
    return crud.delete_receipt(receipt_id=receipt_id)


@app.get(
    "/receipts/{rec_num}",
)
def get_by_recnum(rec_num: str):
    """receipt = crud.get_receipt_by_recnum(rec_num=rec_num)
    json_receipt = jsonable_encoder(receipt)
    print('This is main by recnum func!')"""
    return {"rec_num": rec_num}   #JSONResponse(json_receipt)
