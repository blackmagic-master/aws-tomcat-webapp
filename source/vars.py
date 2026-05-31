import boto3

# specifying the clients used to communicate with AWS
ec2_client = boto3.client('ec2')
route53_client = boto3.client('route53')
elbv_client = boto3.client('elbv2')

# security groups' names
sg_names = {
    "LB": "load-balancer",
    "TOMCAT": "tomcat-server",
    "BACKEND": "backend"
}

# provisioning script files' names
script_files = {
    "TOMCAT": "scripts/tomcat_ubuntu.sh",
    "RABBITMQ": "scripts/rabbitmq.sh",
    "MYSQL": "scripts/mysql.sh",
    "MEMCACHE": "scripts/memcache.sh"
}

# reading the script files
def retrieve_file_contents(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

# placing the contents of the script files into variables
scripts = {
    "TOMCAT": retrieve_file_contents(script_files["TOMCAT"]),
    "RABBITMQ": retrieve_file_contents(script_files["RABBITMQ"]),
    "MYSQL": retrieve_file_contents(script_files["MYSQL"]),
    "MEMCACHE": retrieve_file_contents(script_files["MEMCACHE"])
}

# configuration file of the infrastructure
CONF = "infrastructure.json"