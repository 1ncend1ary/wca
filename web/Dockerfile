#### ------------------------------------------
#### ---- Set up application web component ----:
#### ------------------------------------------
FROM python:3.7

LABEL maintainer="alexseliverstov@yahoo.com"

# Define working directory
WORKDIR /app/web

# Add requirements.txt to container
COPY requirements.txt requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Copy all contents to container
COPY . .

# Run command for production deployment
WORKDIR /app

# Run command in production server environment
CMD cp "$SECRET_WEB" ./web/secret.py && \
    cp "$SECRET_WORD2VEC" ./web/model/GoogleNews-vectors-negative300.bin.gz && \
    gunicorn -b 0.0.0.0:5000 -w 2 --timeout 180 web.main:app


# Uncomment for development environment
#ENV FLASK_APP main.py
#ENV FLASK_RUN_HOST 0.0.0.0
#CMD cp "$SECRET_WEB" ./secret.py && \
#    cp "$SECRET_WORD2VEC" ./model/GoogleNews-vectors-negative300.bin.gz && \
#    flask run
