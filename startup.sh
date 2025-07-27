#!/bin/bash
export PYTHONPATH=/home/site/wwwroot
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
