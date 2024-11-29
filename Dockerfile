# Use an official Python image as a base
FROM python:3.12.6-slim
# Set the working directory in the container
WORKDIR /
# Copy all files from the current directory to the container
COPY . .
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Run migrations and start the development server
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]