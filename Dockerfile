# Dockerfile for the Python script
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY erc20_monitor.py erc20_monitor.py

CMD ["python", "erc20_monitor.py"]
