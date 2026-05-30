import boto3

ec2_client = boto3.client('ec2')
route53_client = boto3.client('route53')

sg_names = {
    "LB": "load-balancer",
    "TOMCAT": "tomcat-server",
    "BACKEND": "backend"
}

script_files = {
    "TOMCAT": "scripts/tomcat_ubuntu.sh",
    "RABBITMQ": "scripts/rabbitmq.sh",
    "MYSQL": "scripts/mysql.sh",
    "MEMCACHE": "scripts/memcache.sh"
}

def retrieve_file_contents(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

scripts = {
    "TOMCAT": retrieve_file_contents(script_files["TOMCAT"]),
    "RABBITMQ": retrieve_file_contents(script_files["RABBITMQ"]),
    "MYSQL": retrieve_file_contents(script_files["MYSQL"]),
    "MEMCACHE": retrieve_file_contents(script_files["MEMCACHE"])
}