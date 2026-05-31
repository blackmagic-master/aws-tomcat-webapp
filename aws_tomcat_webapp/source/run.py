from .vpc import Vpc
from .subnet import Subnet
from .igw import InternetGateway
from .route import RouteTable
from .sec_group import SecurityGroup
from .key import KeyPair
from .ec2 import EC2
from .dns import HostedZone
from .targetgroup import TargetGroup
from .loadbalancer import LoadBalancer
from .vars import *
from .configuration import save_config
import json
import os

def init(config, option):
    # initialize
    vpc = Vpc(config)
    vpc.enable_dns_support()
    subnet1 = Subnet(config, vpc.id, config['vpc']['subnet1'], config['vpc']['az'],)
    subnet2 = Subnet(config, vpc.id, config['vpc']['subnet2'], config['vpc']['alt-az'],)
    igw = InternetGateway(config)
    igw.attach(vpc.id)
    rt = RouteTable(config, vpc.id)
    rt.create_route(igw.id)
    rt.associate(subnet1.id)
    rt.associate(subnet2.id)
    subnet1.enable_public_ip()
    subnet2.enable_public_ip()
    sg = {
        "BACKEND": SecurityGroup(config, vpc.id, sg_names['BACKEND']),
        "TOMCAT": SecurityGroup(config, vpc.id, sg_names['TOMCAT']),
        "LB": SecurityGroup(config, vpc.id, sg_names['LB'])
    }
    sg['LB'].add_allow_port_rule()
    sg['TOMCAT'].add_allow_sg_rule(sg['LB'].id, "TomcatServer")
    sg['BACKEND'].add_allow_sg_rule(sg['TOMCAT'].id, "Backend")
    sg['BACKEND'].add_allow_ssh()
    sg['TOMCAT'].add_allow_ssh()
    sg['TOMCAT'].add_allow_port_rule()
    kp = KeyPair(config)
    ec2 = {
        "MYSQL": EC2(config=config, prefix="MYSQL", kp_name=kp.name, sg_id=sg['BACKEND'].id, subnet_id=subnet1.id, dns_name="db01"),
        "RABBITMQ": EC2(config=config, prefix="RABBITMQ", kp_name=kp.name, sg_id=sg['BACKEND'].id, subnet_id=subnet1.id, dns_name="rmq01"),
        "MEMCACHE": EC2(config=config, prefix="MEMCACHE", kp_name=kp.name, sg_id=sg['BACKEND'].id, subnet_id=subnet1.id, dns_name="mq01"),
        "TOMCAT": EC2(config=config, prefix="TOMCAT", kp_name=kp.name, sg_id=sg['TOMCAT'].id, subnet_id=subnet1.id, dns_name="app01")
    }
    hz = HostedZone(config, vpc.id)
    for instance in ec2:
        hz.create_a_record(ec2[instance].dns_name, ec2[instance].private_ip)
    tg = TargetGroup(config, vpc.id)
    tg.register_targets(ec2['TOMCAT'].id)
    lb = LoadBalancer(config, [subnet1.id, subnet2.id], sg['LB'].id)
    lb.create_listener(tg.arn)
    print("Your application is ready: " + lb.dns_name)
    kp.get()
    # saving the configuration
    save_config(
        config=config,
        vpc=vpc,
        subnets=[subnet1, subnet2],
        igw=igw,
        rt=rt,
        sg=sg,
        kp=kp,
        ec2=ec2,
        hz=hz,
        tg=tg,
        lb=lb
    )
    # clean up
    if option == "T":
        while True:
            inp = input("Are you ready to remove all the built infrastructure? (Y/n): ")
            if inp.lower() == "y" or inp.lower() == "yes":
                break
            else:
                print("Okay, waiting for 'yes' answer...")
        lb.delete_listener()
        lb.remove()
        tg.deregister_targets(ec2['TOMCAT'].id)
        tg.remove()
        for instance in ec2:
            hz.delete_a_record(ec2[instance].dns_name, ec2[instance].private_ip)
        hz.remove()
        for instance in ec2:
            ec2[instance].remove()
        kp.remove()
        for group in sg:
            sg[group].remove()
        rt.disassociate()
        rt.delete_route()
        rt.remove()
        igw.detach(vpc.id)
        igw.remove()
        subnet1.remove()
        subnet2.remove()
        vpc.remove()
def destroy(config):
    file = open(CONF, 'r')
    configuration = json.load(file)
    file.close()
    elbv_client.delete_listener(
        ListenerArn=configuration['LoadBalancer']['ListenerArn']
    )
    elbv_client.delete_load_balancer(
        LoadBalancerArn=configuration['LoadBalancer']['Arn']
    )
    elbv_client.deregister_targets(
        TargetGroupArn=configuration['TargetGroup']['Arn'],
        Targets=[
            {
                'Id': configuration['Instances'][3]['Id'],
                'Port': 8080
            }
        ]
    )
    elbv_client.delete_target_group(
        TargetGroupArn=configuration['TargetGroup']['Arn'],
    )
    for instance in configuration['Instances']:
        route53_client.change_resource_record_sets(
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': {
                            'Name': instance['DnsName'] + "." +
                            configuration['HostedZone']['Name'],
                            'ResourceRecords': [
                                {
                                    'Value': instance['PrivateIpAddress']
                                },
                            ],
                            'TTL': 60,
                            'Type': 'A',
                        },
                    },
                ],
                'Comment': 'Web server for example.com',
            },
            HostedZoneId=configuration['HostedZone']['Id'],
        )
    route53_client.delete_hosted_zone(
        Id=configuration['HostedZone']['Id']
    )
    for instance in configuration['Instances']:
        ec2_client.terminate_instances(
            InstanceIds=[
                instance['Id'],
            ],
            Force=True,
            SkipOsShutdown=True
        )
        waiter = ec2_client.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=[instance['Id']])
    ec2_client.delete_key_pair(
        KeyName=configuration['KeyPair']['Name'],
        KeyPairId=configuration['KeyPair']['Id']
    )
    for group in configuration['SecurityGroups']:
        ec2_client.delete_security_group(
            GroupId=group['Id'],
            GroupName=group['Name']
        )
    for association in configuration['RouteTable']['AssociationIds']:
        ec2_client.disassociate_route_table(
            AssociationId=association
        )
    ec2_client.delete_route(
        RouteTableId=configuration['RouteTable']['Id'],
        DestinationCidrBlock=configuration['RouteTable']['DestinationCidrBlock']
    )
    ec2_client.delete_route_table(
        RouteTableId=configuration['RouteTable']['Id']
    )
    ec2_client.detach_internet_gateway(
        InternetGatewayId=configuration['InternetGateway']['Id'],
        VpcId=configuration['VPC']['Id']
    )
    ec2_client.delete_internet_gateway(
        InternetGatewayId=configuration['InternetGateway']['Id']
    )
    for subnet in configuration['Subnets']:
        ec2_client.delete_subnet(
            SubnetId=subnet['Id']
        )
    ec2_client.delete_vpc(VpcId=configuration['VPC']['Id'])
    if os.path.exists(CONF):
        os.remove(CONF)
    else:
        print("The file does not exist: " + CONF)
    if os.path.exists(config['KeyPair']['file']):
        os.remove(config['KeyPair']['file'])
    else:
        print("The file does not exist: " + config['KeyPair']['file'])
    print("Cleanup was completed successfully.")