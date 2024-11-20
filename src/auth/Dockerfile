FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir django djangorestframework djangorestframework-simplejwt celery django-celery-results psycopg2-binary django-environ sentry-sdk

EXPOSE 8000

# Run the application:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
