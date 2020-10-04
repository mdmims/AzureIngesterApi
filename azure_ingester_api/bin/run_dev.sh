#!/usr/bin/env bash

export SQLALCHEMY_DATABASE_URI=sqlite:////tmp/testdb.sqlite

# Run database migrations
python manage.py db upgrade

# Start the server
python manage.py runserver