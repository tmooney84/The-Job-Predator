FROM python:3.11-slim

WORKDIR /app/scraper_orchestrator/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY scraper_orchestrator/requirements.txt .

# Debug: Check if file is there
RUN ls -l /app
RUN cat requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire scraper_orchestrator folder
COPY scraper_orchestrator/ /app/scraper_orchestrator

#CMD ["python3", "publisher_main.py"]
CMD ["python3", "publisher_service.py"]