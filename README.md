
# Building A Dash App And Deploying it on Google Cloud Run (GCR) with an Example

## Prerequisites

- You need a Google Cloud account with a project set up and billing-enabled.
- You need the GCR CLI installed.
- You need to have Docker installed locally.

## 1. Steps for Setup

When your app is ready and working locally, you can proceed to the next steps. This example uses a simple Dash app with a singular graph. The complexity of the app is not the primary focus of this script.

There are two essential parts of the Python code required for your app to work on GCR:

```python
# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Expose the Flask instance (required for Gunicorn)
# This is super important and app.server is what you call in the docker
server = app.server
```

Additionally, ensure you have the following block at the end of your script to bind the app to the correct port for Google Cloud Run:

```python
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(host='0.0.0.0', port=port)
```

Once you have your app running, open the terminal in the app's directory and test it works by running:

```bash
python app.py
```

If everything works fine, you can proceed to build your Dockerfile.

## 2. Check or Build the Dockerfile

Docker Image: Think of a Docker image like a blueprint or a recipe. It's a file that contains everything your app needs to run, including the app code, system libraries, and dependencies (like Python or Dash). But, it's not running yet—it's just the instructions.

Docker Container: A Docker container is like a fully built version of that image, now "alive" and running. It uses the blueprint (the image) to run your app in a completely isolated environment, so it works the same no matter where it's running—on your computer, in the cloud, or anywhere else.

Ensure your `Dockerfile` is correctly set up to build the Dash app with Gunicorn. Here's an example of what the `Dockerfile` should look like:

```Dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for the port (needed for Cloud Run)
ENV PORT=8080

# Run the application with Gunicorn
CMD ["gunicorn", "-b", ":8080", "app:app"]
```

## 3. Build the Docker Image

Now, build the Docker image locally. Ensure Docker is running on your machine and execute the following command:

```bash
docker build -t my-dash-app:latest .
```

You can name the app anything you like. The `latest` refers to the version you're building, and the `.` refers to the current directory.

This will build the Docker image and tag it as `my-dash-app:latest`. Tags are important for keeping version control of the Docker image.

## 4. Run the Docker Container Locally

Run the container locally using the following command:

```bash
docker run -p 8080:8080 my-dash-app:latest
```

This will run the container and expose port `8080`. Once it’s running, open [http://127.0.0.1:8080/](http://127.0.0.1:8080/) in your browser to check if the app is accessible.

If this step doesn't work but your app worked locally, you likely have an issue with the `requirements.txt` or the `Dockerfile`.

## 5. Troubleshooting – Skip if Successful

If you're having issues, you can use the following command to access the container's shell for additional debugging:

```bash
docker run -it my-dash-app:latest /bin/bash
```

Make necessary changes and rebuild the Docker image. Anytime you change something, you must rebuild the Docker image.

## 6. Clean up Local Docker Files (USE WITH CAUTION)

If you need to clean up Docker images to free up space, proceed with caution as this can remove valuable images. 

To remove all dangling images (untagged images):

```bash
docker image prune
```

To remove all unused images, even if they are tagged:

```bash
docker image prune -a
```

Additionally, to clean up unused containers, networks, and volumes, run:

```bash
docker system prune -a --volumes
```

## 7. Tag Your Docker Image for Google Container Registry (GCR)

Before deploying to Cloud Run, you’ll need to push your Docker image to Google Container Registry (GCR). First, tag the image with the GCR registry location. Replace `[PROJECT-ID]` with your actual Google Cloud project ID:

```bash
docker tag my-dash-app gcr.io/[PROJECT-ID]/my-dash-app:latest
```

Example:

```bash
docker tag my-dash-app gcr.io/my-first-project/my-dash-app:latest
```

## 8. Push the Docker Image to GCR

Once the image is tagged, push it to Google Container Registry:

```bash
docker push gcr.io/[PROJECT-ID]/my-dash-app:latest
```

Example:

```bash
docker push gcr.io/my-first-project/my-dash-app:latest
```

This will upload your Docker image to GCR.

## 9. Deploy to Google Cloud Run

Once the image is in GCR, you can deploy it to Cloud Run:

```bash
gcloud run deploy my-dash-app     --image gcr.io/[PROJECT-ID]/my-dash-app:latest     --platform managed     --region [REGION]     --allow-unauthenticated     --port 8080
```

Explanation:

- `my-dash-app`: The name of your Cloud Run service.
- `gcr.io/[PROJECT-ID]/my-dash-app:latest`: The Docker image from GCR.
- `--platform managed`: Specifies Cloud Run fully managed.
- `--region [REGION]`: The region where you want to deploy (e.g., `us-central1`).
- `--allow-unauthenticated`: Allows public access to your app. Remove this if you want it to be private.
- `--port 8080`: The port your Dash app is listening on.

## 10. Access the App

Once the deployment is successful, Cloud Run will give you a URL where you can access your Dash app.

You can retrieve the URL with:

```bash
gcloud run services describe my-dash-app --platform managed --region [REGION] --format 'value(status.url)'
```

## 11. Optional: Monitor and Scale the App

Google Cloud Run automatically scales your app based on traffic. However, you can also set minimum and maximum instance counts or configure autoscaling. For example:

```bash
gcloud run services update my-dash-app --min-instances 1 --max-instances 10
```
