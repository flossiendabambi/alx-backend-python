# Base image
FROM python:3.10

# Set working directory in container
WORKDIR /app

# Copy everything from outer directory into container (access manage.py)
COPY ../ /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r messaging_app/requirements.txt

# Expose Django default port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

