import boto3

ec2_client = boto3.client('ec2')

sg_names = {
    "LB": "load-balancer",
    "TOMCAT": "tomcat-server",
    "BACKEND": "backend"
}