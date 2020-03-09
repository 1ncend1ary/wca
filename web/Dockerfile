#### ------------------------------------------
#### ---- Set up application web component ----:
#### ------------------------------------------
FROM python:3.7

MAINTAINER Aleksei Seliverstov <alexseliverstov@yahoo.com>

# Define working directory.
WORKDIR /app/web

# Set up environment variables for Flask.
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0

# Install required libraries.
#RUN apk add --no-cache gcc musl-dev linux-headers
#RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.5/community" >> /etc/apk/repositories; \
#    echo "http://dl-2.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories; \
#    echo "http://dl-3.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories; \
#    echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories; \
#    echo "http://dl-5.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories;
#
#RUN apk update \
#  && apk add --no-cache libblas-dev liblapack-dev lapack-dev

# Add requirements.txt to container.
COPY requirements.txt requirements.txt

# Install requirements.
RUN pip install -r requirements.txt

# Copy all contents to container
COPY . .

# Set default command.
CMD ["flask", "run"]
