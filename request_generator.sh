#!/bin/bash
while true
do
  curl --silent -H "Content-Type: application/json" --data @request.json http://localhost:8087/webhook > /dev/null
  echo "request send"
	sleep 5
done
