FROM docker.io/python:3.7.4-alpine3.10

RUN apk add --no-cache bash && \
    pip3 --no-cache-dir install influxdb urllib3 beautifulsoup4 certifi

COPY ./main.py /app/main.py

ENV INFLUXDB_HOST="scraping_and_grafana_influxdb_1" \
    INFLUXDB_PORT="8086" \
    INFLUXDB_DATABASE="mydb"