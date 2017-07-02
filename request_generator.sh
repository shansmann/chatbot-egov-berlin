#!/bin/bash
while true
do
  curl -H "Content-Type: application/json" --data @request.json http://0.0.0.0:8087/webhook
  echo "request send"
	sleep 5
done
