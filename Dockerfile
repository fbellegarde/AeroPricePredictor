# Use an official Python runtime as a parent image
# We choose a lightweight image based on Debian 12 (bookworm)
FROM python:3.12-slim-bookworm

# 1. Set the working directory in the container
WORKDIR /usr/src/app

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app

# 3. Copy dependencies list and install dependencies
# We copy requirements.txt first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application source code
# This includes the 'app' folder, 'data' folder, and training scripts
COPY . .

# 5. EXPOSE the port the app runs on (Flask default is 5000)
EXPOSE 5000

# 6. Define the command to run the application (Gunicorn is production standard)
# We use Gunicorn to serve the Flask app because it's robust and handles multiple workers.
# The command structure is: gunicorn -b 0.0.0.0:5000 <module_name>:<application_instance>
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]