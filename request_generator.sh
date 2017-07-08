#!/bin/bash
while true
do
  curl -H "Content-Type: application/json" --data @fake_request.json http://0.0.0.0:8085/webhook
  echo "request send"
	sleep 5
done
