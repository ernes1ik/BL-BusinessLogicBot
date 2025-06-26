FROM python:3.9-slim

WORKDIR /app

# Создаем папку для данных
RUN mkdir -p /app/data

# Копируем код
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота
CMD ["python", "bot_runner.py"]