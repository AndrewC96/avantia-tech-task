#!/bin/bash
set -e

echo "Waiting for MongoDB to be ready..."
while ! mongosh --eval "db.runCommand('ping').ok" \
    --host mongodb \
    --username "$MONGO_USER" \
    --password "$MONGO_PASSWORD" \
    --authenticationDatabase admin \
    >/dev/null 2>&1; do
    sleep 2
done

echo "MongoDB is ready, running data ingestion..."
python db_ingest.py

echo "Verifying data ingestion..."
python test_ingestion.py

echo "Starting Flask application..."
python app.py