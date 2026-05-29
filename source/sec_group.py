from .vars import *
from .checks import check_if_true

class SecurityGroup:
    def __init__(self, config, vpc_id, prefix):
        self.config = config
        self.name = config['ProjectName'] + "-" + prefix + "-sg"
        self.vpc_id = vpc_id
        self.sg = ec2_client.create_security_group(
            GroupName=self.name,
            Description=f"Security group for {config['ProjectName']}",
            VpcId=self.vpc_id
        )
        self.id = self.sg['GroupId']
    def add_allow_port_rule(self):
        for port in self.config['vpc']['ports']:
            check_if_true(
                ec2_client.authorize_security_group_ingress(
                    GroupId=self.id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': port,
                            'ToPort': port,
                            'IpRanges': [
                                {
                                    'CidrIp': self.config['vpc']['dest-cidr'],
                                }
                            ]
                        }
                    ]
                )
            )
    def add_allow_sg_rule(self, sg_id, service):
        for port in self.config[service]['Ports']:
            check_if_true(
                ec2_client.authorize_security_group_ingress(
                    GroupId=self.id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': port,
                            'ToPort': port,
                            'UserIdGroupPairs': [
                                {
                                    'GroupId': sg_id
                                },
                            ],
                        },
                    ]
                )
            )
    def add_allow_ssh(self):
        check_if_true(
            ec2_client.authorize_security_group_ingress(
                GroupId=self.id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [
                            {
                                'CidrIp': self.config['vpc']['dest-cidr'],
                            }
                        ]
                    }
                ]
            )
        )
    def remove(self):
        check_if_true(
            ec2_client.delete_security_group(
                GroupId=self.id,
                GroupName=self.name
            )
        )