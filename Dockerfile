# Используем базовый образ с Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную окружения для порта
ENV PORT 2005

# Открываем порт в контейнере
EXPOSE $PORT

# Запускаем ваше приложение
CMD ["uvicorn", "api_application:app", "--host", "0.0.0.0", "--port", "2000"]
