from .vpc import *
from .subnet import *
from .igw import *
from .route import *
from .sec_group import *
from .key import *
from .ec2 import *

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
    kp = KeyPair(config)
    ec2 = EC2(config, "BACKEND", kp.name, sg['BACKEND'].id, subnet.id)
    # kp.get()
    #
    # # clean up
    con = input()
    ec2.remove()
    kp.remove()
    sg['BACKEND'].remove()
    sg['TOMCAT'].remove()
    sg['LB'].remove()
    rt.disassociate()
    rt.delete_route()
    rt.remove()
    igw.detach(vpc.id)
    igw.remove()
    subnet.remove()
    vpc.remove()