# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8080

# Define environment variable for the port (needed for Cloud Run)
ENV PORT=8080

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:server"]