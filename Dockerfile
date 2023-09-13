FROM python:latest

# Disable buffering for Python, enabling real-time log output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./ /app

RUN pip install --no-cache-dir -r requirements.txt

RUN alembic stamp head
RUN alembic revision --autogenerate -m "create tables"
RUN alembic upgrade head

ENTRYPOINT ["./master_data.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

