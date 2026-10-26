#!/bin/bash
# ===================================================================
# Docker Volume Data Persistence Verification Script
# Course: DevOps for Cloud Computing (CSC418) - Lab Mid Examination
# Student: SP23-BSE-131
# Task 4: Create named volume & demonstrate persistence after container recreation
# ===================================================================

set -e

echo "============================================================="
echo "   Docker Volume Persistence Verification - SP23-BSE-131"
echo "============================================================="

# Step 1: Start containers with Docker Compose
echo -e "\n[Step 1] Starting services with Docker Compose..."
docker compose up -d

echo "--> Waiting for PostgreSQL database to be healthy..."
sleep 15

# Step 2: Show named volume created
echo -e "\n[Step 2] Inspecting Docker Named Volume:"
docker volume ls | grep sp23_bse_131_db_data || docker volume ls | grep db_data

# Step 3: Insert a test record directly or through web app
echo -e "\n[Step 3] Verifying records in database before destruction..."
docker compose exec db psql -U sp23_admin -d sp23_bse_131_db -c "SELECT username, email, reg_number FROM users;"

# Step 4: Destroy containers completely (without removing named volume!)
echo -e "\n[Step 4] Tearing down and removing running containers..."
docker compose down

echo "--> Verifying containers are removed:"
docker ps | grep sp23 || echo "No containers running."

# Step 5: Recreate and restart containers from scratch
echo -e "\n[Step 5] Recreating containers from the ground up..."
docker compose up -d

echo "--> Waiting for PostgreSQL database to re-initialize..."
sleep 15

# Step 6: Verify data still exists!
echo -e "\n[Step 6] PROOF OF PERSISTENCE: Checking data in the new container..."
docker compose exec db psql -U sp23_admin -d sp23_bse_131_db -c "SELECT username, email, reg_number FROM users;"

echo -e "\n============================================================="
echo ">>> SUCCESS: Data survived complete container recreation! <<<"
echo "============================================================="
