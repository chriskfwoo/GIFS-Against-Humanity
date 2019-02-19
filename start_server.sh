#!/bin/bash

cd server && source venv/bin/activate && source .env 
kill -9 `cat app.pid`
gunicorn --bind 0.0.0.0:5000 --worker-class gevent -w 1 wsgi:app --daemon -p app.pid