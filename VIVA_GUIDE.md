# Section B: Viva Preparation & Concept Guide (15 Marks)

**Course:** DevOps for Cloud Computing (CSC418)  
**Instructor:** Dr. M. Hasanain Ch  
**Student:** SP23-BSE-131  
**Viva Date:** 28 October 2026  

---

## 1. AWS EC2, Load Balancing & Auto Scaling Concepts [3 Marks]

### Q1: What is the role of an Application Load Balancer (ALB) in this architecture?
- **Answer:** The ALB operates at **Layer 7 (Application Layer)** of the OSI model. It acts as the single point of entry for user traffic, distributing incoming requests across multiple EC2 instances running in different Availability Zones.
- It performs **Health Checks** on `/health` every 15 seconds. If an instance becomes unhealthy, the ALB stops routing traffic to it, ensuring zero-downtime and high availability.

### Q2: How does an Auto Scaling Group (ASG) work with the Load Balancer?
- **Answer:** The ASG automatically manages the EC2 fleet size according to demand.
  - In our setup: **Desired: 2, Min: 2, Max: 4**.
  - When traffic increases (CPU utilization exceeds 70%), ASG provisions additional EC2 instances from the Launch Template.
  - As soon as the new instance passes the ALB target group health check, ALB automatically adds it to the routing pool without manual intervention.

### Q3: Why place EC2 instances in multiple Availability Zones?
- **Answer:** Fault tolerance. If an AWS datacenter (AZ-1) experiences an outage, instances in AZ-2 continue serving requests seamlessly through the ALB.

---

## 2. Linux Commands & File Permissions [2 Marks]

### Q1: Explain the permissions `chmod 755` and `chmod 700` used in your setup script.
- **Answer:** Linux permissions follow an octal notation `rwx` (read=4, write=2, execute=1):
  - **`755` (`rwxr-xr-x`)**: Owner has read, write, execute (7); Group has read and execute (5); Others have read and execute (5). Used for application directories and public executables.
  - **`700` (`rwx------`)**: Only the owner has read, write, execute; Group and Others have zero permissions. Used for sensitive data directories and database storage to prevent unauthorized inspection.

### Q2: Why create a dedicated service user with `useradd -r -s /bin/false`?
- **Answer:** Following the **Principle of Least Privilege (PoLP)** and security hardening:
  - `-r` creates a system user with a low UID.
  - `-s /bin/false` prevents direct interactive login shell access. If a container or app process is compromised, the attacker cannot log into the host OS shell.

---

## 3. Docker Images, Dockerfile & Containers [3 Marks]

### Q1: What is the difference between a Docker Image and a Docker Container?
- **Answer:**
  - An **Image** is a read-only, immutable snapshot/blueprint created from a `Dockerfile` containing application code, runtime dependencies, and environment settings.
  - A **Container** is a live, runnable instance of an image with an added thin read-write layer and isolated process namespace.

### Q2: How did you optimize your custom Dockerfile?
- **Answer:**
  1. **Minimal Base Image:** Used `python:3.11-slim` rather than full python to minimize image size and attack surface.
  2. **Layer Caching:** Copied `requirements.txt` and ran `pip install` *before* copying the full application source code. When code changes, Docker reuses cached pip dependencies, making builds 10x faster.
  3. **Non-Root Execution:** Created user `appuser` and switched to `USER appuser` so the container does not run as root.
  4. **Health Probe:** Added `HEALTHCHECK` checking `/health` every 30s.

---

## 4. Docker Volumes & Data Persistence [2 Marks]

### Q1: Why are container filesystems ephemeral by default, and how do named volumes solve this?
- **Answer:** Containers are stateless by design; any data written to the container layer is destroyed when the container is deleted (`docker rm` or `docker compose down`).
- A **Named Volume** (`sp23_bse_131_db_data`) is managed directly by the Docker engine on the host filesystem outside the container union filesystem. When the container restarts or is recreated, the volume is remounted to `/var/lib/postgresql/data`, preserving all database tables, users, and tasks without loss.

### Q2: How do you demonstrate volume persistence during evaluation?
- **Answer:**
  1. Start app: `docker compose up -d`
  2. Register user & add a task.
  3. Teardown: `docker compose down` (proves containers are destroyed).
  4. Recreate: `docker compose up -d`
  5. Refresh browser: User account and task remain intact.

---

## 5. Docker Compose & Multi-Container Communication [3 Marks]

### Q1: How do the `web` container and `db` container communicate without hardcoded IP addresses?
- **Answer:** Docker Compose creates a custom user-defined bridge network (`sp23_bse_131_network`).
- Docker provides built-in **DNS resolution**: the `web` container connects to the database simply using the service name `db` (e.g. `postgresql://sp23_admin:...@db:5432/sp23_bse_131_db`).

### Q2: What is the purpose of `depends_on` with `condition: service_healthy`?
- **Answer:** PostgreSQL takes 5-10 seconds to initialize schemas. If the web app starts immediately, it crashes with "connection refused".
- `condition: service_healthy` guarantees that the `web` container waits until PostgreSQL passes `pg_isready` before starting Gunicorn.

---

## 6. Selenium Testing & Test Execution [2 Marks]

### Q1: What does your automated Selenium script test?
- **Answer:**
  1. Opens landing page and asserts project title and student registration badge `SP23-BSE-131`.
  2. Automates student registration (`/auth/register`) with generated test credentials.
  3. Automates login (`/auth/login`) and asserts dashboard welcome banner.
  4. Interacts with the Kanban task board: clicks modal, submits a task, and asserts the task title is rendered in the DOM.
  5. Queries the ALB health endpoint `/health` verifying 200 OK.

### Q2: How can Selenium run in a headless CI/CD or cloud environment?
- **Answer:** By setting Chrome/Edge options `--headless=new`, `--no-sandbox`, and `--disable-dev-shm-usage`. The browser runs completely in memory without requiring a physical monitor or GUI display.
