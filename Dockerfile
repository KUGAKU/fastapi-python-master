FROM python:latest

# Disable buffering for Python, enabling real-time log output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./ /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["./master_data.sh"]

