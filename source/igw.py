from .vars import *
from .checks import check_response

# Internet Gateway class
class InternetGateway:
    # initializing an internet gateway
    def __init__(self, config):
        self.config = config
        self.vpc_id = None
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
        print("Created an internet gateway: " + self.name + " " + self.id)
    # attaching the internet gateway to the VPC
    def attach(self, vpc_id):
        self.vpc_id = vpc_id
        ec2_client.attach_internet_gateway(
            InternetGatewayId=self.id,
            VpcId=self.vpc_id
        )
    # detaching the internet gateway from the VPC
    def detach(self, vpc_id):
        self.vpc_id = vpc_id
        ec2_client.detach_internet_gateway(
            InternetGatewayId=self.id,
            VpcId=vpc_id
        )
    # removing the internet gateway
    def remove(self):
        check_response(
            ec2_client.delete_internet_gateway(
                InternetGatewayId=self.id
            )
        )