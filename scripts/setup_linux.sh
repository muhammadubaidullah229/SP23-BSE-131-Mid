#!/bin/bash
# ===================================================================
# Linux Administration & Permissions Setup Script
# Course: DevOps for Cloud Computing (CSC418) - Lab Mid Examination
# Student: SP23-BSE-131
# Task 2: Execute basic Linux commands, create directory, configure permissions
# ===================================================================

set -e

echo "=== [Task 2: Linux Administration Script Started] ==="

# 1. Update system package index
echo "--> Updating package repository..."
sudo apt-get update -y

# 2. Create Application Directory under /opt (Standard Linux production directory)
APP_DIR="/opt/SP23-BSE-131-Mid"
echo "--> Creating dedicated application directory: $APP_DIR"
sudo mkdir -p "$APP_DIR"
sudo mkdir -p "$APP_DIR/data"
sudo mkdir -p "$APP_DIR/logs"

# 3. Create dedicated non-login service user for security
SERVICE_USER="deployer_sp23"
if id "$SERVICE_USER" &>/dev/null; then
    echo "--> User $SERVICE_USER already exists."
else
    echo "--> Creating service user: $SERVICE_USER"
    sudo useradd -r -s /bin/false "$SERVICE_USER"
fi

# 4. Configure File and Directory Permissions (Principle of Least Privilege)
echo "--> Configuring directory and file permissions..."
# Set ownership of application files to service user
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"

# Set directory permissions: rwxr-xr-x (755)
sudo chmod 755 "$APP_DIR"
sudo chmod 755 "$APP_DIR/logs"

# Set sensitive data directory permissions: rwx------ (700)
sudo chmod 700 "$APP_DIR/data"

# Verify permissions
echo "--> Verifying configured permissions:"
ls -ld "$APP_DIR"
ls -ld "$APP_DIR/data"
ls -ld "$APP_DIR/logs"

echo "=== [Task 2: Linux Administration Setup Completed Successfully] ==="
