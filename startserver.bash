#!/bin/bash

export MONGOURI="mongodb+srv://asxlvm:A6wRgGs5INzVXdYw@cluster0.nm2p7.mongodb.net"
export PORT="8080"
echo "[INFO] Exported environment variables, starting ($(TZ='Europe/Prague' date) - $(TZ='Europe/Prague' date +%s))"

/usr/bin/python3 manage.py runserver $PORT
