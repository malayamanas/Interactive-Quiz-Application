#!/bin/bash

# Step 1: Make migrations
echo "Making migrations..."
python manage.py makemigrations

# Step 2: Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Step 3: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput  # --noinput prevents the script from asking for confirmation

echo "Django management commands executed successfully!"
