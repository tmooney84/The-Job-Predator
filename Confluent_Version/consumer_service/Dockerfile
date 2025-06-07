FROM python:3.11-slim
WORKDIR /app/consumer_service
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \  
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the app code
COPY Confluent_Version/consumer_service/ /app/consumer_service

# Copy the models into the container
COPY Confluent_Version/models /app/consumer_service/models

COPY Confluent_Version/consumer_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



#CMD ["python3", "consumer_main.py"]
CMD ["python3", "consumer_service.py"]