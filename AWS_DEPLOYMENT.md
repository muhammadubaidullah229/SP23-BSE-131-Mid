# AWS Load Balancer & Auto Scaling Group Deployment Guide

**Course:** DevOps for Cloud Computing (CSC418) - Lab Mid Examination  
**Student:** SP23-BSE-131  
**Project:** SP23-BSE-131-Mid  

---

## 1. Architecture Overview

```
                      [ User / Client Browser ]
                                  │
                                  ▼
               [ AWS Application Load Balancer (ALB) ]
                         (DNS Name / Port 80)
                                  │
                ┌─────────────────┴─────────────────┐
                ▼                                   ▼
   [ EC2 Instance 1 (AZ-1) ]           [ EC2 Instance 2 (AZ-2) ]
   ┌───────────────────────┐           ┌───────────────────────┐
   │ Docker Compose        │           │ Docker Compose        │
   │ ├── Web App (Port 5000)│           │ ├── Web App (Port 5000)│
   │ └── PostgreSQL DB     │           │ └── PostgreSQL DB     │
   │     (Named Volume)    │           │     (Named Volume)    │
   └───────────────────────┘           └───────────────────────┘
                ▲                                   ▲
                └─────────────────┬─────────────────┘
                                  │
                   [ Auto Scaling Group (ASG) ]
                   (Min: 2, Desired: 2, Max: 4)
```

---

## 2. Step-by-Step Implementation Instructions

### Step 1: Create Security Groups
1. **ALB Security Group (`sp23-alb-sg`)**:
   - Inbound: HTTP (Port 80) from `0.0.0.0/0`
   - Inbound: HTTPS (Port 443) from `0.0.0.0/0`
   - Outbound: All Traffic (`0.0.0.0/0`)

2. **EC2 Application Security Group (`sp23-ec2-sg`)**:
   - Inbound: Custom TCP (Port 5000) from source `sp23-alb-sg` (Ensures traffic only arrives through Load Balancer)
   - Inbound: SSH (Port 22) from My IP (for administrative access)
   - Outbound: All Traffic (`0.0.0.0/0`)

---

### Step 2: Create Target Group
1. Go to **EC2 Console** &rarr; **Target Groups** &rarr; **Create target group**.
2. Target type: **Instances**.
3. Target group name: `sp23-bse-131-tg`.
4. Protocol: **HTTP**, Port: **5000**.
5. VPC: Select default or project VPC.
6. **Health Check Settings**:
   - Health check protocol: `HTTP`
   - Health check path: `/health`
   - Healthy threshold: `2`
   - Unhealthy threshold: `2`
   - Timeout: `5 seconds`
   - Interval: `15 seconds`
   - Success code: `200`
7. Click **Create target group**.

---

### Step 3: Create Application Load Balancer (ALB)
1. In EC2 Console, select **Load Balancers** &rarr; **Create Load Balancer** &rarr; **Application Load Balancer**.
2. Name: `sp23-bse-131-alb`.
3. Scheme: **Internet-facing**, IP address type: **IPv4**.
4. Network Mapping: Select VPC and check at least **2 Availability Zones** (e.g. `us-east-1a`, `us-east-1b`).
5. Security groups: Select `sp23-alb-sg`.
6. Listeners and routing:
   - Protocol: `HTTP`, Port: `80`.
   - Default action: Forward to target group `sp23-bse-131-tg`.
7. Click **Create load balancer**. Note down the **ALB DNS Name** (e.g., `sp23-bse-131-alb-123456789.us-east-1.elb.amazonaws.com`).

---

### Step 4: Create EC2 Launch Template with User Data
1. Go to **Launch Templates** &rarr; **Create launch template**.
2. Name: `sp23-bse-131-launch-template`.
3. AMI: **Ubuntu Server 22.04 LTS (HVM)** or **Amazon Linux 2023**.
4. Instance type: `t2.micro` or `t3.micro` (Free tier eligible).
5. Security group: `sp23-ec2-sg`.
6. In **Advanced Details** &rarr; **User Data**, paste the startup provisioning script:

```bash
#!/bin/bash
# User Data Script for Auto Scaling Instance Initialization
apt-get update -y
apt-get install -y docker.io docker-compose git

# Start and enable Docker
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# Clone student repository
mkdir -p /opt/app
cd /opt/app
git clone https://github.com/your-username/SP23-BSE-131-Mid.git .

# Start multi-container application
docker-compose up -d --build
```

7. Click **Create launch template**.

---

### Step 5: Create Auto Scaling Group (ASG)
1. Go to **Auto Scaling Groups** &rarr; **Create Auto Scaling group**.
2. Name: `sp23-bse-131-asg`.
3. Launch template: Select `sp23-bse-131-launch-template`.
4. Network: Select project VPC and both Availability Zones.
5. In **Load balancing**, select **Attach to an existing load balancer** &rarr; Choose `sp23-bse-131-tg`.
6. Enable **ELB Health checks** (Grace period: `300 seconds`).
7. **Group Size & Scaling Policies**:
   - Desired capacity: `2`
   - Minimum capacity: `2`
   - Maximum capacity: `4`
8. Target tracking policy: Metric type: **Average CPU utilization (Target: 70%)**.
9. Click **Create Auto Scaling group**.

---

### Step 6: Verification & Demonstration
1. In EC2 Console &rarr; **Target Groups** &rarr; verify both instances show status **Healthy**.
2. Open the ALB DNS URL in a browser:
   `http://sp23-bse-131-alb-123456789.us-east-1.elb.amazonaws.com`
3. Verify landing page with registration badge `SP23-BSE-131` loads and all functionalities operate through the load balancer.
4. Run Selenium automated tests against the ALB DNS URL:
   ```powershell
   $env:APP_URL="http://sp23-bse-131-alb-123456789.us-east-1.elb.amazonaws.com"
   python tests/test_selenium.py
   ```
