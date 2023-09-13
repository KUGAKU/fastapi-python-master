FROM python:latest

# Disable buffering for Python, enabling real-time log output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./ /app

# Make the script executable and run it
RUN chmod +x master_data.sh && ./master_data.sh

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]

