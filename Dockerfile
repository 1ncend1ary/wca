FROM python:3.7-alpine


MAINTAINER Aleksei Seliverstov <alexseliverstov@yahoo.com>

WORKDIR /code

ENV FLASK_APP web/main.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]
