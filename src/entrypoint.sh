#!/bin/sh

echo "Waiting for postgresql to start..."

while ! nc -z db 5432; do
    sleep 0.1
done

echo "Postgresql started successfully"
exec "$@"