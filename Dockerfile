FROM python:3.12.6-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (PostgreSQL and others)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend application
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
