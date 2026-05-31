# AWS Tomcat Web Application Orchestrator

A Python-based Infrastructure as Code (IaC) automation tool that provisions, configures, and destroys a highly available multi-tier web application architecture on Amazon Web Services (AWS).

This project is now distributed as a **versioned Python package**, available via **GitHub Releases** and installable through `pip`. It can also be built locally as a standard Python package.

---

## Overview

This tool automates deployment of a full AWS-based web application stack, including:

* Application Load Balancer (ALB)
* Apache Tomcat application server
* MariaDB / MySQL database
* RabbitMQ message broker
* Memcached cache layer
* Route 53 private hosted zone
* Full VPC networking (subnets, routing, security groups)

---

## Package installation

### Install via pip (recommended)

Download the latest release and install directly:

```bash
pip install aws-tomcat-webapp
```

Or install a specific version:

```bash
pip install aws-tomcat-webapp==1.0.1
```

---

### Install from GitHub Release (wheel or tar.gz)

Download the asset from the **Releases page**, then install:

```bash
pip install aws_tomcat_webapp-1.0.1-py3-none-any.whl
```

or:

```bash
pip install aws_tomcat_webapp-1.0.1.tar.gz
```

---

### Build from source

You can also build the package locally:

```bash
git clone https://github.com/blackmagic-master/aws-tomcat-webapp.git
cd aws-tomcat-webapp

python -m build
```

Then install the generated artifact:

```bash
pip install dist/aws_tomcat_webapp-*.whl
```

---

## CLI usage

After installation, the orchestrator is available as a command-line tool:

### Deploy infrastructure

**Permanent deployment:**

```bash
aws-webapp up --permanent
# or
aws-webapp up -p
```

**Temporary deployment:**

```bash
aws-webapp up --temporary
# or
aws-webapp up -t
```

---

### Destroy infrastructure

```bash
aws-webapp down
```

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

## Private DNS mappings

* `db01.aws-webapp.hz` → Database endpoint
* `rmq01.aws-webapp.hz` → Message broker endpoint
* `mc01.aws-webapp.hz` → Cache layer endpoint

---

## Configuration

Configuration is managed through `config.json`.

Example:

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
    "ports": [80]
  },
  "KeyPair": {
    "file": "keypair.pem"
  },
  "TomcatServer": {
    "Ports": [8080]
  },
  "Backend": {
    "Ports": [3306, 11211, 5672]
  },
  "Ec2": {
    "BackendAmi": "ami-xxxxxxxxxxxx",
    "TomcatAmi": "ami-xxxxxxxxxxxx"
  }
}
```

---

## AWS authentication

Before using the tool, configure AWS credentials:

```bash
aws configure
```

Ensure the IAM user/role has permissions for:

* EC2
* VPC
* ELB / ALB
* Route 53
* Security Groups
* IAM (limited keypair operations)

---

## State & artifacts

During execution, the package generates local state files:

* `infrastructure.json` → tracks deployed resources
* `keypair.pem` → generated EC2 key pair

Do not modify or delete `infrastructure.json`, as it is required for safe teardown.

---

## Example output

```text
Created route table: aws-webapp-rt rtb-xxxxxxxx
Created security group: aws-webapp-LB-sg sg-xxxxxxxx
Created security group: aws-webapp-TOMCAT-sg sg-xxxxxxxx
Created security group: aws-webapp-BACKEND-sg sg-xxxxxxxx

Deployment complete:
aws-webapp-lb-xxxxxxxx.us-east-1.elb.amazonaws.com
```

---

## Development & packaging

To rebuild the package locally:

```bash
python -m build
```

To install in editable mode for development:

```bash
pip install -e .
```

---

## Author

BlackMagic Master
Szymon G