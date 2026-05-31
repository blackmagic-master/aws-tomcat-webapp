# AWS Tomcat Web Application Orchestrator

A Python-based Infrastructure as Code (IaC) automation tool that provisions, configures, and destroys a highly available multi-tier web application architecture on Amazon Web Services (AWS).

## Overview

This project deploys:

- Application Load Balancer (ALB)
- Apache Tomcat application server
- MariaDB/MySQL database
- RabbitMQ message broker
- Memcached cache server
- Route 53 private hosted zone
- VPC, subnets, security groups, and routing infrastructure

---

## Architecture

```text
                        Internet
                            |
                            v
                 +-------------------+
                 | Application Load  |
                 |    Balancer       |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |     Tomcat App    |
                 |      Port 8080    |
                 +----+---------+----+
                      |         |
          +-----------+         +-----------+
          |                                 |
          v                                 v
+-------------------+             +-------------------+
| MariaDB / MySQL   |             | RabbitMQ          |
| Port 3306         |             | Port 5672         |
+-------------------+             +-------------------+

                +-------------------+
                | Memcached         |
                | Port 11211        |
                +-------------------+

```

---

## Prerequisites

Ensure your environment meets the following baseline requirements:

* **Python 3.x**
* **AWS CLI** configured with proper administrative access keys.
* An active **AWS Account**.

### Install dependencies

```bash
pip install boto3 requests

```

---

## Usage

### Deploy infrastructure

**Permanent deployment:**

```bash
python aws-tomcat-webapp.py up --permanent
# OR
python aws-tomcat-webapp.py up -p

```

**Temporary deployment:**

```bash
python aws-tomcat-webapp.py up --temporary
# OR
python aws-tomcat-webapp.py up -t

```

### Destroy infrastructure

```bash
python aws-tomcat-webapp.py down

```

---

### Private DNS mappings

* `db01.aws-webapp.hz` (Database entrypoint)
* `rmq01.aws-webapp.hz` (Message broker entrypoint)
* `mc01.aws-webapp.hz` (Caching layer entrypoint)

---

## Example output

```text
Created a route table: aws-webapp-rt rtb-xxxxxxxx
Created a security group: aws-webapp-LB-sg sg-xxxxxxxx
Created a security group: aws-webapp-TOMCAT-sg sg-xxxxxxxx
Created a security group: aws-webapp-BACKEND-sg sg-xxxxxxxx

Your application is ready:
aws-webapp-lb-xxxxxxxx.us-east-1.elb.amazonaws.com

```

---

## Configuration

All architectural parameters, network layouts, and Amazon Machine Images (AMIs) are centrally managed via the `config.json` file in the root directory.

### AWS authentication (required)

Before running the orchestration tool, you must authenticate your local environment with your AWS credentials. The automation script leverages your local AWS CLI profile settings to securely invoke AWS APIs.

Run the following command and input your AWS Access Key, Secret Key, and default region:

```bash
aws configure

```

**Important:** The IAM entity used must have sufficient administrative permissions to provision core infrastructure, including custom VPCs, EC2 instances, Application Load Balancers, Route 53 zones, and Security Groups.

---

### The `config.json` structure

The project includes a pre-configured configuration file. You can adjust CIDR blocks, opening ports, and AMI selections directly within `config.json`:

```json
{
  "ProjectName": "aws-webapp",
  "vpc": {
    "cidr": "10.10.0.0/16",
    "subnet1": "10.10.10.0/24",
    "subnet2": "10.10.20.0/24",
    "az": "us-east-1a",
    "alt-az": "us-east-1b",
    "dest-cidr": "0.0.0.0/0",
    "ports": [
      80
    ]
  },
  "KeyPair": {
    "file": "keypair.pem"
  },
  "TomcatServer": {
    "Ports": [
      8080
    ]
  },
  "Backend": {
    "Ports": [
      3306,
      11211,
      5672
    ]
  },
  "Ec2": {
    "BackendAmi": "ami-00e801948462f718a",
    "TomcatAmi": "ami-091138d0f0d41ff90"
  }
}

```

* **`ProjectName`**: Serves as the naming prefix for AWS tags and resource labels. It is also used to derive the name of the EC2 Key Pair in AWS.
* **`vpc`**: Controls network segmentation, setting target Availability Zones (`az`, `alt-az`) and the edge load balancer inbound port (`80`).
* **`KeyPair`**: Declares the local destination file name for the generated SSH private key.
* **`TomcatServer` / `Backend**`: Explicit lists of internal ports mapped automatically to respective security groups.
* **`Ec2`**: Contains fixed AMI IDs for the application tier and backend databases. *(Verify these are active IDs in your chosen region).*

---

### State & asset artifacts

When you initialize a deployment using `python aws-tomcat-webapp.py up`, the orchestration tool automatically generates state artifacts in your local directory:

* **Automated Key Pair Management:** The tool dynamically provisions a new AWS EC2 Key Pair using your `ProjectName`. The associated private key file (e.g., `keypair.pem`) is written straight to your root folder. Keep this private key secure to access your compute instances later.
* **`infrastructure.json`:** This file serves as your environment's local state registry. It stores live instance IDs, VPC routing details, service configuration variables, and reference metadata for every provisioned cloud resource.

**Critical Key Pair Conflict Check:** Before initiating a deployment, ensure that your target AWS region **does not** already have an existing Key Pair with a name matching your `ProjectName` (or a duplicate local key file). The script will fail or risk overriding configurations if a name collision occurs.

**Note:** Do not modify or delete `infrastructure.json`. The teardown tool (`python aws-tomcat-webapp.py down`) relies strictly on this file to locate, map, and cleanly remove your provisioned stack without leaving orphaned resources.

---

## Author
BlackMagic Master
Szymon G,