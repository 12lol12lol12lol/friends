FROM python:3.10.9-alpine3.17

RUN apk add --update --no-cache --virtual buld-base postgresql-dev gcc \
 python3-dev musl-dev

WORKDIR /project
COPY . /project
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
WORKDIR /project/src
CMD ["sh", "-c",  "./manage.py collectstatic --no-input && ./manage.py migrate && gunicorn --bind 0.0.0.0:8000 \
         --reload \
         --timeout 600 \
         src.wsgi:application"]