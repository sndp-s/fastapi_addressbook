# Import python image
FROM python:3.9-slim

# Setup working dir in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the fastapi code into the container
COPY . .

# Expose port 80
EXPOSE 80

# Command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
