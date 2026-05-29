from .vars import *
from .checks import check_response

class Vpc:
    def __init__(self, config):
        self.config = config
        self.name = config['ProjectName'] + "-vpc"
        self.vpc = ec2_client.create_vpc(
            CidrBlock=self.config['vpc']['cidr'],
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': self.name
                        }
                    ]
                }
            ]
        )
        self.id = self.vpc['Vpc']['VpcId']

    def enable_dns_support(self):
        check_response(
            ec2_client.modify_vpc_attribute(
                EnableDnsHostnames={
                    'Value': True
                },
                VpcId=self.vpc['Vpc']['VpcId']
            )
        )
        check_response(
            ec2_client.modify_vpc_attribute(
                EnableNetworkAddressUsageMetrics={
                    'Value': False
                },
                VpcId=self.id
            )
        )
    def remove(self):
        check_response(
            ec2_client.delete_vpc(VpcId=self.id)
        )