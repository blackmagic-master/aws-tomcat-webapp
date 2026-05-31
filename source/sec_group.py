from .vars import *
from .checks import check_if_true

# Security group class
class SecurityGroup:
    # initializing a security group
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
        print("Created a security group: " + self.name + " " + self.id)
    # adding 'ALLOW' rule for the specified port
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
    # adding 'ALLOW' rule for the specified security group
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
    # adding 'ALLOW' rule for ssh connections
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
    # removing the security group
    def remove(self):
        check_if_true(
            ec2_client.delete_security_group(
                GroupId=self.id,
                GroupName=self.name
            )
        )