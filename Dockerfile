# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create a non-root user named 'dockeruser'
RUN useradd -m dockeruser

# Set permissions for the application files
COPY . /app
RUN chown -R dockeruser:dockeruser /app

# Switch to the non-root user 'dockeruser'
USER dockeruser

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the Flask
CMD ["python", "flask_app.py"]
