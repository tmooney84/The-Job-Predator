# Use official Python runtime image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the models into the image
COPY ../models /app/models

# Copy the app code
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
