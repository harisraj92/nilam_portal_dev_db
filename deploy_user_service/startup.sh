#!/bin/bash
pip install -r requirements.txt
exec uvicorn user_service.main:app --host 0.0.0.0 --port 8000
