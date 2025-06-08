# Use the official Python image
FROM python:3.10-slim

# Working directory inside the container
WORKDIR /app

# Copy dependencies and install (if requirements.txt exists)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Default command (can be empty, we will run manually via make)
CMD ["python", "main.py"]
