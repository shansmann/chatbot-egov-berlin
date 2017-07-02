#!/bin/bash
while true
do
  curl -H "Content-Type: application/json" --data @request.json http://localhost:8087/webhook
  echo "request send"
	sleep 5
done
