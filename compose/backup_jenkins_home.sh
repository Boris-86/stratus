#!/bin/bash

# Check if a container ID or name was provided
if [ -z "$1" ]; then
    echo "[ERROR] Usage: $0 <container_id_or_name>"
    exit 1
fi

CONTAINER_ID="$1"
DEST_DIR="./jenkins_home_backup"

echo "[INFO] Backing up Jenkins home directory from container: $CONTAINER_ID"
echo "[INFO] Destination: $DEST_DIR"

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Copy /var/jenkins_home from container to local machine
docker cp "${CONTAINER_ID}:/var/jenkins_home/." "$DEST_DIR"

# Check if the copy succeeded
if [ $? -eq 0 ]; then
    echo "[SUCCESS] Backup completed successfully."
else
    echo "[ERROR] Failed to copy Jenkins home from container."
    exit 1
fi
