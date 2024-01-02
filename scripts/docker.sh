#!/bin/bash

# Check if Docker is installed and available
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install it."
    exit 1
fi

# Check the status of Docker
status=$(systemctl is-active docker)

if [ "$status" == "active" ]; then
    echo "Docker is running."
else
    echo "Docker is not running."
fi
