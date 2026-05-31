import json
from .vars import *

def save_config(config, vpc, subnets, igw, rt, sg, kp, ec2, hz, tg, lb):
    configuration = {
        "VPC": {
            "Name": vpc.name,
            "Id": vpc.id
        },
        "Subnets": [
            {
                "Name": subnets[0].name,
                "Id": subnets[0].id
            },
            {
                "Name": subnets[1].name,
                "Id": subnets[1].id
            }
        ],
        "InternetGateway": {
            "Name": igw.name,
            "Id": igw.id
        },
        "RouteTable": {
            "Name": rt.name,
            "Id": rt.id,
            "AssociationIds": rt.association_id,
            "DestinationCidrBlock": config['vpc']['dest-cidr']
        },
        "SecurityGroups": [
            {
                "Name": sg['BACKEND'].name,
                "Id": sg['BACKEND'].id
            },
            {
                "Name": sg['TOMCAT'].name,
                "Id": sg['TOMCAT'].id
            },
            {
                "Name": sg['LB'].name,
                "Id": sg['LB'].id
            }
        ],
        "KeyPair": {
            "Name": kp.name,
            "Id": kp.id
        },
        "Instances": [
            {
                "Name": ec2['MYSQL'].name,
                "Id": ec2['MYSQL'].id,
                "SecurityGroupId": ec2['MYSQL'].sg_id,
                "PrivateIpAddress": ec2['MYSQL'].private_ip,
                "DnsName": ec2['MYSQL'].dns_name
            },
            {
                "Name": ec2['RABBITMQ'].name,
                "Id": ec2['RABBITMQ'].id,
                "SecurityGroupId": ec2['RABBITMQ'].sg_id,
                "PrivateIpAddress": ec2['RABBITMQ'].private_ip,
                "DnsName": ec2['RABBITMQ'].dns_name
            },
            {
                "Name": ec2['MEMCACHE'].name,
                "Id": ec2['MEMCACHE'].id,
                "SecurityGroupId": ec2['MEMCACHE'].sg_id,
                "PrivateIpAddress": ec2['MEMCACHE'].private_ip,
                "DnsName": ec2['MEMCACHE'].dns_name
            },
            {
                "Name": ec2['TOMCAT'].name,
                "Id": ec2['TOMCAT'].id,
                "SecurityGroupId": ec2['TOMCAT'].sg_id,
                "PrivateIpAddress": ec2['TOMCAT'].private_ip,
                "DnsName": ec2['TOMCAT'].dns_name
            }
        ],
        "HostedZone": {
            "Name": hz.name,
            "Id": hz.id
        },
        "TargetGroup": {
            "Name": tg.name,
            "Arn": tg.arn
        },
        "LoadBalancer": {
            "Name": lb.name,
            "Arn": lb.arn,
            "ListenerArn": lb.listener_arn,
            "DNSName": lb.dns_name
        }
    }
    file = open(CONF, 'w')
    file.write(json.dumps(configuration))
    file.close()
    print("Configuration saved to " + CONF)