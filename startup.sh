#!/bin/sh
redis-server &
uvicorn 'app.app:app' --host=0.0.0.0 --port=8080