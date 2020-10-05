#!/usr/bin/env bash

export API_ENVIRONMENT=azure_ingester_api.config.TestConfig
export SQLALCHEMY_DATABASE_URI=sqlite:////tmp/testdb.sqlite
export FLASK_ENV=development

# Run database migrations
python manage.py db upgrade

# Start the server
python manage.py runserver