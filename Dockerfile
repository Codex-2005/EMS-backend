# Use an official Python runtime as a parent image
FROM python:3.12.6-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (PostgreSQL and others)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt . 

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend application
COPY . .

# Expose the port that Django app will run on
EXPOSE 8000

# Run migrations, collect static files, and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 your_project_name.wsgi:application"]
