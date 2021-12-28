#!/bin/bash
cd ~/pi-automations/InteractionAPI
value=$(<api_flask.pid)
echo "Killing $value"
kill -9 "$value"
