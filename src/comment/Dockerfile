FROM python:3.9

ENV DJANGO_ENV=production

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir django djangorestframework celery django-celery-results requests psycopg2-binary django-environ

EXPOSE 8000

# Run the application:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
