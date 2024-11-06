# hyves-back-end
This is the back-end of the Reviving Hyves project. It is a RESTful API that is built using Django REST framework. This API is used to store and retrieve data from the database. The data is used by the front-end to display the information to the user.

## Installation
Python version 3.12
Django version 4.2
Django REST framework version 3.15.2

## Usage
To start a microservice in de /src folder, run the following command
```bash
cd src/[microservice]
python manage.py runserver 0.0.0.0:[port]
```
The lists of ports per microservice:
- 8001: comment
- 8002: auth
- 8003: post

To build with docker and run the container, run the following command
```bash
cd src/
docker-compose up --build
```

---
```By Nick Welles```