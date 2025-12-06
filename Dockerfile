FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Создание статических файлов (без зависимостей от настроек)
# Сначала проверяем, что manage.py работает
RUN python -c "import django; print(f'Django version: {django.__version__}')"

# Временные переменные для сборки
ENV DJANGO_SETTINGS_MODULE=django_app.settings
ENV DJANGO_SECRET_KEY=temp_key_for_build_only
ENV POSTGRES_DB=temp
ENV POSTGRES_USER=temp
ENV POSTGRES_PASSWORD=temp
ENV DJANGO_DEBUG=False

# Попытка собрать статические файлы, если не получается - продолжаем
RUN python manage.py collectstatic --noinput --settings=django_app.settings || \
    echo "⚠️  Static collection failed, continuing anyway..."

# Порт для Gunicorn
EXPOSE 8000

# Скрипт для запуска
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:8000 --workers 3 django_app.wsgi:application"]
