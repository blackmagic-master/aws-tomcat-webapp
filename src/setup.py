from .vars import *
from .init_key import create_keypair, delete_keypair
from .init_vpc import *
from .init_subnet import *
from .init_igw import *
from .init_rt import *
from .init_sec_group import *
from .init_key import *

def init(config):
    vpc = Vpc(config)
    vpc.enable_dns_support()
    subnet = Subnet(config, vpc.id)
    igw = InternetGateway(config)
    igw.attach(vpc.id)
    rt = RouteTable(config, vpc.id)
    rt.create_route(igw.id)
    rt.associate(subnet.id)
    subnet.enable_public_ip()
    sg = SecurityGroup(config, vpc.id)
    sg.add_allow_rule()

    sg.remove()
    rt.disassociate()
    rt.delete_route()
    rt.remove()
    igw.detach(vpc.id)
    igw.remove()
    subnet.remove()
    vpc.remove()

    # keypair = create_keypair(names['keypair'])
    #
    # delete_keypair(names['keypair'], keypair['KeyPairId'])