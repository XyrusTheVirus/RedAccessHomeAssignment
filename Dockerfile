FROM python:3.11-slim

WORKDIR /app

# Create venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better Docker cache use
COPY requirements.txt /app/requirements.txt

# Copy app and scripts
COPY app/ /app/
COPY scripts/start.sh /app/start.sh
COPY migrations/ /app/migrations/
COPY mongo_migrate.json /app/mongo_migrate.json

RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]