from .vars import *
from .checks import check_if_true

class SecurityGroup:
    def __init__(self, config, vpc_id):
        self.config = config
        self.name = config['ProjectName'] + "-sg"
        self.vpc_id = vpc_id
        self.port = config['vpc']['port']
        self.sg = ec2_client.create_security_group(
            GroupName=self.name,
            Description=f"Security group for {config['ProjectName']}",
            VpcId=self.vpc_id
        )
        self.id = self.sg['GroupId']
    def add_allow_rule(self):
        check_if_true(
            ec2_client.authorize_security_group_ingress(
                GroupId=self.id,
                IpProtocol='tcp',
                FromPort=self.port,
                ToPort=self.port,
                CidrIp=self.config['vpc']['dest-cidr']
            )
        )
    def remove(self):
        check_if_true(
            ec2_client.delete_security_group(
                GroupId=self.id,
                GroupName=self.name
            )
        )