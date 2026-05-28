from .vars import *
from .checks import check_response

class Subnet:
    def __init__(self, config, vpc_id):
        self.config = config
        self.vpc_id = vpc_id
        self.name = config['ProjectName'] + "-subnet"
        self.subnet = ec2_client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=self.config['vpc']['cidr'],
            AvailabilityZone=self.config['vpc']['az'],
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': self.name
                        }
                    ]
                }
            ]
        )
        self.id = self.subnet['Subnet']['SubnetId']
    def enable_public_ip(self):
        ec2_client.modify_subnet_attribute(
            SubnetId=self.id,
            MapPublicIpOnLaunch={'Value': True}
        )
    def remove(self):
        check_response(
            ec2_client.delete_subnet(
                SubnetId=self.id
            )
        )