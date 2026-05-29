from .vars import *
from .checks import check_response

class RouteTable:
    def __init__(self, config, vpc_id):
        self.igw_id = None
        self.assosiation_id = None
        self.vpc_id = vpc_id
        self.subnet_id = None
        self.config = config
        self.name = config['ProjectName'] + "-rt"
        self.rt = ec2_client.create_route_table(
            VpcId=self.vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'route-table',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': self.name
                        }
                    ]
                }
            ]
        )
        self.id = self.rt['RouteTable']['RouteTableId']
    def create_route(self, igw_id):
        self.igw_id = igw_id
        check_response(
            ec2_client.create_route(
                RouteTableId=self.id,
                DestinationCidrBlock=self.config['vpc']['dest-cidr'],
                GatewayId=self.igw_id
            )
        )
    def delete_route(self):
        check_response(
            ec2_client.delete_route(
                RouteTableId=self.id,
                DestinationCidrBlock=self.config['vpc']['dest-cidr']
            )
        )
    def associate(self, subnet_id):
        self.subnet_id = subnet_id
        self.assosiation_id = ec2_client.associate_route_table(
            RouteTableId=self.id,
            SubnetId=self.subnet_id
        )['AssociationId']
    def disassociate(self):
        check_response(
            ec2_client.disassociate_route_table(
                AssociationId=self.assosiation_id
            )
        )
    def remove(self):
        check_response(
            ec2_client.delete_route_table(
                RouteTableId=self.id
            )
        )
