trap 'kill %1;' SIGINT SIGTERM EXIT
poetry run python manage.py runserver &
poetry run daphne -b 0.0.0.0 -p 8001 backend.asgi:application --application-close-timeout 120
