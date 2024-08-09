# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . .

# Expose the port (Cloud Run uses the PORT environment variable)
ENV PORT 8080
EXPOSE 8080

# Run migrations and collect static files
RUN python manage.py migrate

# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "fs_api.wsgi"]
