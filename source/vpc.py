from .vars import *
from .checks import check_response

# VPC class
class Vpc:
    # initializing a VPC
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
        print("Created a VPC: " + self.name + " " + self.id)
    # adding the DNS support for the VPC
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
    # removing the VPC
    def remove(self):
        check_response(
            ec2_client.delete_vpc(VpcId=self.id)
        )