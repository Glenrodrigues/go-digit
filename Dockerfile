# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir boto3==1.24.28 pandas SQLAlchemy==1.4.22 numpy

# Copy the current directory contents into the container at /app
COPY . .

EXPOSE 80

CMD ["python", "main.py"]