# fastapi-python-master

## how to start

1. run `python -m venv venv`
2. run `source venv/bin/activate`
3. run `pip install -r requirements.txt`
4. run Run and Debug in VSCode

## how to add model

1. create models/xxx.py
2. run `$ alembic revision --autogenerate -m "create tables"`
3. run `alembic upgrade head`

## how to use

1. run `docker build -t fastapi-python-master .`
2. run `docker run -d -p 8000:8000 -v $(pwd):/app --env-file .env --name fastapi-python-master-container fastapi-python-master`

## How to run test

1. run `pytest`
