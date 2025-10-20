FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc libpq-dev wget unzip curl netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Flyway
RUN wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.16.0/flyway-commandline-9.16.0-linux-x64.tar.gz \
    | tar xvz && \
    mv flyway-9.16.0 /opt/flyway && \
    ln -s /opt/flyway/flyway /usr/local/bin/flyway
WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install --upgrade pip \
    && pip install "poetry==1.8.3" \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . /app
COPY wait_for_kafka.py /app/wait_for_kafka.py

EXPOSE 81
CMD ["sh", "-c", "python /app/wait_for_services.py && uvicorn src.main:app --host 0.0.0.0 --port 81"]


