FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir django djangorestframework

EXPOSE 8000

# Run the application:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
