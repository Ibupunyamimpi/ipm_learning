# Use the specified Python version
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE your_project_name.settings.production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY ./requirements /app/requirements/
RUN pip install --upgrade pip \
    && pip install -r /app/requirements/production.txt

# Copy the application code to the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the app
CMD ["gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
