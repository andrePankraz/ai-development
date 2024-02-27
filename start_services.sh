#!/bin/bash

# Start the initai_inference_service.service
python3 -m ai_development.service &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
