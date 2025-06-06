FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \  
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the models into the container
COPY Confluent_Version/models /app/models

COPY Confluent_Version/consumer_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY Confluent_Version/consumer_service/ /app

CMD ["python3", "consumer_main.py"]
