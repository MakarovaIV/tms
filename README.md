# TMS (Test Management System) 
## Description
Application for QA Engineer for storage and maintain test artifacts (test-cases, test-plans and reports).

Stack:
- Django 4
- Bootstrap 5
- JQuery 3.7

Role model contains 'Owner', 'Developer' and 'Tester'. 
'Owner' has full access to all objects.
'Tester' has access to view and modify suits, test-cases, test-plans and reports.
'Developer' access is read-only.

Features:
- Create and modify projects, suits and test-cases
- Create test-plans
- Create reports based on test-plans results

## Run app
- Clone repo
- Install requirements
```commandline
pip install -r requirements.txt
```
- Set up PostgreSQL DB (change username, pass and db name)
```commandline
docker run --name pg_db -p 5432:5432 -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=test_password -e POSTGRES_DB=test_db -d postgres:15.2
```
- Make migrations (run command from directory `tms/management_system`)
```commandline
python3 manage.py migrate
```
- Run Django server
```commandline
python3 manage.py runserver
```

## Run unit tests
```commandline
python3 manage.py test
```

## Tutorial
View examples [here](Tutorial.md).