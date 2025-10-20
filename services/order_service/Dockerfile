FROM python:3.10-slim

# system deps for building Python extensions and postgres client libs
RUN apt-get update && apt-get install -y \
    gcc libpq-dev wget unzip curl netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Flyway for database migrations
RUN wget https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.19.0/flyway-commandline-10.19.0-linux-x64.tar.gz \
    && tar -xzf flyway-commandline-10.19.0-linux-x64.tar.gz \
    && mv flyway-10.19.0 /usr/local/flyway \
    && ln -s /usr/local/flyway/flyway /usr/local/bin/flyway \
    && rm flyway-commandline-10.19.0-linux-x64.tar.gz

WORKDIR /app

# Copy dependency files first (for docker layer cache)
COPY pyproject.toml poetry.lock* /app/

# Install Poetry 1.x and project deps
RUN pip install --upgrade pip \
    && pip install "poetry==1.8.3" \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy code and wait script
COPY . /app
COPY wait_for_kafka.py /app/wait_for_kafka.py

EXPOSE 80

# Wait for Kafka, then start Uvicorn
CMD ["sh", "-c", "python /app/wait_for_kafka.py && uvicorn src.main:app --host 0.0.0.0 --port 80"]

