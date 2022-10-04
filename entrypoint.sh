#!/usr/bin/env bash
setsid docker-entrypoint.sh postgres >/dev/fd/1 2>&1 < /dev/fd/1 &

sleep 10
/usr/bin/python3.7 global_functions.py initialize-db
/usr/local/bin/gunicorn -b 0.0.0.0:9090 seclyzer.app:app --workers=1 --threads=10 --timeout 1800