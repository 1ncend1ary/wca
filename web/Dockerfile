#### ------------------------------------------
#### ---- Set up application web component ----:
#### ------------------------------------------
FROM python:3.7

MAINTAINER Aleksei Seliverstov <alexseliverstov@yahoo.com>

# Define working directory
WORKDIR /app/web

# Add requirements.txt to container
COPY requirements.txt requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Copy all contents to container
COPY . .

# Uncomment for development environment
#ENV FLASK_APP main.py
#ENV FLASK_RUN_HOST 0.0.0.0
#CMD ["flask", "run"]

# Run command for production deployment
WORKDIR /app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "web.main:app"]
