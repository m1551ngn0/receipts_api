FROM python:alpine

WORKDIR /home/receipts-api/main
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

COPY __init__.py main.py boot.sh ./
COPY app app
COPY databases databases
RUN chmod +x boot.sh

ENTRYPOINT ["./boot.sh"]
