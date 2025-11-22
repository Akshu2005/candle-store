#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE=candle_shop.settings

echo "Starting Gunicorn server..."
gunicorn candle_shop.wsgi:application --bind 0.0.0.0:$PORT --workers 3
