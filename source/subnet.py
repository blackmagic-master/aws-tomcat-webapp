from .vars import *
from .checks import check_response

# Subnet class
class Subnet:
    # initializing a subnet
    def __init__(self, config, vpc_id, cidr, az):
        self.config = config
        self.vpc_id = vpc_id
        self.name = config['ProjectName'] + "-subnet"
        self.cidr = cidr
        self.az = az
        self.subnet = ec2_client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=self.cidr,
            AvailabilityZone=self.az,
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
        print("Created a subnet: " + self.name + " " + self.id)
    # allowing the subnet to get a public IP address
    def enable_public_ip(self):
        ec2_client.modify_subnet_attribute(
            SubnetId=self.id,
            MapPublicIpOnLaunch={'Value': True}
        )
    # removing the subnet
    def remove(self):
        check_response(
            ec2_client.delete_subnet(
                SubnetId=self.id
            )
        )