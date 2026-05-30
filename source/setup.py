from .vpc import *
from .subnet import Subnet
from .igw import *
from .route import *
from .sec_group import *
from .key import *
from .ec2 import EC2
from .dns import *
from .targetgroup import *
from .loadbalancer import *

def init(config):
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
    print(lb.dns_name)
    # kp.get()
    #
    # # clean up
    con = input()
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