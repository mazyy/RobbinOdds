# Start from the official Airflow image (version pinned to match your docker-compose)
FROM apache/airflow:2.10.5

USER root
# Optionally install system dependencies needed by Scrapy or other packages.
# RUN apt-get update && apt-get install -y \
#     libssl-dev libxml2-dev libxslt1-dev libz-dev \
#     # etc. -- add more as needed for your scrapers
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user to install Python dependencies
USER airflow

# Copy your requirements into the container
COPY requirements.txt /tmp/requirements.txt

# Install them. If you rely on .env for dynamic requirements, you can do it that way instead.
RUN pip install --no-cache-dir -r /tmp/requirements.txt
