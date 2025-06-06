# Use official Python runtime image
FROM python:3.11-slim

# Set working directory in container
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

# Copy requirements.txt into the container
COPY Confluent_Version/frontend/requirements.txt . 

# Install dependencies
RUN ls -l /app
RUN pip install --no-cache-dir -r requirements.txt


# Copy the models into the container
COPY Confluent_Version/models /app/models

# Copy the frontend app code
COPY Confluent_Version/frontend/ /app

# Expose port 6300
EXPOSE 6300

# Run the Flask app
CMD ["python3", "app.py"]