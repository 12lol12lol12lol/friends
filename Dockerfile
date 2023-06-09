FROM python:3.10.9-alpine3.17

RUN apk add buld-base

COPY . app/
WORKDIR /app
RUN pip install -r requirements.txt