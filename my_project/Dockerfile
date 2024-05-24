# Устанавливаем базовый образ, который содержит все необходимое для запуска Django приложения
FROM python:3.12

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

WORKDIR /app

COPY . .

RUN chmod 777 ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]