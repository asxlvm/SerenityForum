#!/bin/bash

export MONGOURI="mongodb+srv://asxlvm:A6wRgGs5INzVXdYw@cluster0.nm2p7.mongodb.net"

echo "[INFO] Exported environment variables, starting ($(TZ='Europe/Prague' date) - $(TZ='Europe/Prague' date +%s))"

python3 manage.py runserver 0.0.0.0:$PORT
