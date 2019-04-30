#!/bin/bash
while true; do
  python seriallog.py
  python clf_handio_predict.py
  sleep 5
done
