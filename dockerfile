FROM python:3.10-alpine

WORKDIR /app

# نصب کتابخانه‌های سیستمی مورد نیاز برای mysqlclient
RUN apk add --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps gcc musl-dev mariadb-dev \
    && pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# حذف بسته‌های build-deps پس از نصب
RUN apk del .build-deps

COPY . /app/

CMD [ "python","manage.py","runserver","0.0.0.0:8000"]