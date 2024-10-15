FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir django djangorestframework

EXPOSE 8001

# Run the application:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
