from .vpc import *
from .subnet import *
from .igw import *
from .route import *
from .sec_group import *
from .key import *
from .ec2 import *
from .dns import *

def init(config):
    # initialize
    vpc = Vpc(config)
    vpc.enable_dns_support()
    subnet = Subnet(config, vpc.id)
    igw = InternetGateway(config)
    igw.attach(vpc.id)
    rt = RouteTable(config, vpc.id)
    rt.create_route(igw.id)
    rt.associate(subnet.id)
    subnet.enable_public_ip()

    sg = {
        "LB": SecurityGroup(config, vpc.id, sg_names['LB']),
        "TOMCAT": SecurityGroup(config, vpc.id, sg_names['TOMCAT']),
        "BACKEND": SecurityGroup(config, vpc.id, sg_names['BACKEND'])
    }
    sg['LB'].add_allow_port_rule()
    sg['TOMCAT'].add_allow_sg_rule(sg['LB'].id, "TomcatServer")
    sg['BACKEND'].add_allow_sg_rule(sg['TOMCAT'].id, "Backend")
    sg['BACKEND'].add_allow_ssh()
    sg['TOMCAT'].add_allow_ssh()
    sg['TOMCAT'].add_allow_port_rule()
    kp = KeyPair(config)
    ec2 = {
        "MYSQL": EC2(config=config, prefix="MYSQL", kp_name=kp.name, sg_id=sg['BACKEND'].id, subnet_id=subnet.id, dns_name="db01"),
        "RABBITMQ": EC2(config=config, prefix="RABBITMQ", kp_name=kp.name, sg_id=sg['BACKEND'].id, subnet_id=subnet.id, dns_name="rmq01"),
        "MEMCACHE": EC2(config=config, prefix="MEMCACHE", kp_name=kp.name, sg_id=sg['BACKEND'].id, subnet_id=subnet.id, dns_name="mq01"),
        "TOMCAT": EC2(config=config, prefix="TOMCAT", kp_name=kp.name, sg_id=sg['TOMCAT'].id, subnet_id=subnet.id, dns_name="app01")
    }
    hz = HostedZone(config, vpc.id)
    for instance in ec2:
        hz.add_a_record(ec2[instance].dns_name, ec2[instance].private_ip)
    # kp.get()
    #
    # # clean up
    con = input()
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
    subnet.remove()
    vpc.remove()