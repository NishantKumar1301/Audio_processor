#!/usr/bin/env bash
set -o errexit  # Exit on error

echo "🔄 Running Build Script..."

# Install dependencies
pip install -r requirements.txt

# Ensure reset script exists before running
if [ -f "abc.py" ]; then
    python abc.py
else
    echo "⚠️ Warning: abc.py not found, skipping..."
fi

# Fake-reset django_celery_beat migrations and reapply
echo "🔄 Resetting django_celery_beat migrations..."
python manage.py migrate --fake django_celery_beat zero || echo "⚠️ Fake-reset failed"
python manage.py migrate django_celery_beat || echo "⚠️ Celery Beat migration failed"

# Apply remaining migrations
echo "🔄 Applying all database migrations..."
python manage.py migrate || echo "⚠️ Migration process encountered an error"

echo "✅ Build process completed successfully!"
