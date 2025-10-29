# Set base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip &&\
	pip install --no-cache-dir -r requirements.txt

# Add user
RUN useradd -m kalika

# Copy application code
COPY --chown=kalika:kalika . .

# Switch to non-root user
USER kalika

# Expose port
ENV APP_PORT=8000
EXPOSE ${APP_PORT}

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
