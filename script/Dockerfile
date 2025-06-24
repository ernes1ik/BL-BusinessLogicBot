FROM python:3.9-slim

WORKDIR /app

# Создаем отдельную папку для БД
RUN mkdir -p /app/data

# Копируем только необходимые файлы
COPY ./script ./script
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Указываем рабочую директорию для БД
ENV DB_PATH=/app/data/bot_db.sqlite

CMD ["python", "-m", "script.main"]

