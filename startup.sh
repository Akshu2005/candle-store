#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE=config.settings

echo "Starting Gunicorn server..."
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3
