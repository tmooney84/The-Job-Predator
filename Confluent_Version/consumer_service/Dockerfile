FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../models /app/models

COPY . .

CMD ["python3", "consumer_main.py"]
