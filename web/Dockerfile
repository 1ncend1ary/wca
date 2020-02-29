#### ------------------------------------------
#### ---- Set up application web component ----:
#### ------------------------------------------
FROM python:3.7-alpine

MAINTAINER Aleksei Seliverstov <alexseliverstov@yahoo.com>

# Define working directory.
WORKDIR /app/web

# Set up environment variables for Flask.
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0

# Install required libraries.
RUN apk add --no-cache gcc musl-dev linux-headers

# Add requirements.txt to container.
COPY requirements.txt requirements.txt

# Install requirements.
RUN pip install -r requirements.txt

# Copy all contents to container
COPY . .

# Set default command.
CMD ["flask", "run"]