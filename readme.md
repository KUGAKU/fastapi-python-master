# fastapi-python-master

## how to start

1. run `pip install -r requirements.txt`
2. run Debug and Execute in VSCode

## how to add model

1. create models/xxx.py
2. run `$ alembic revision --autogenerate -m "create tables"`
3. run `alembic upgrade head`

## how to use

1. run `docker build -t fastapi-python-master .`
2. run `docker run --name fastapi-python-master-container -p 8000:8000 fastapi-python-master`

## How to run test

1. run `pytest`
