from .vars import *
from .checks import check_response

class InternetGateway:
    def __init__(self, config):
        self.config = config
        self.name = config['ProjectName'] + "-igw"
        self.igw = ec2_client.create_internet_gateway(
            TagSpecifications=[
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': self.name
                        }
                    ]
                }
            ]
        )
        self.id = self.igw['InternetGateway']['InternetGatewayId']
    def attach(self, vpc_id):
        self.vpc_id = vpc_id
        ec2_client.attach_internet_gateway(
            InternetGatewayId=self.id,
            VpcId=self.vpc_id
        )
    def detach(self, vpc_id):
        self.vpc_id = vpc_id
        ec2_client.detach_internet_gateway(
            InternetGatewayId=self.id,
            VpcId=vpc_id
        )
    def remove(self):
        check_response(
            ec2_client.delete_internet_gateway(
                InternetGatewayId=self.id,
            )
        )