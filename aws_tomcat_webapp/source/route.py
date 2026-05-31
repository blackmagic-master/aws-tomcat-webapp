from .vars import *
from .checks import check_response

# Route table class
class RouteTable:
    # initializing a route table
    def __init__(self, config, vpc_id):
        self.igw_id = None
        self.association_id = []
        self.vpc_id = vpc_id
        self.subnet_id = None
        self.config = config
        self.name = self.config['ProjectName'] + "-rt"
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
        print("Created a route table: " + self.name + " " + self.id)
    # creating a route
    def create_route(self, igw_id):
        self.igw_id = igw_id
        check_response(
            ec2_client.create_route(
                RouteTableId=self.id,
                DestinationCidrBlock=self.config['vpc']['dest-cidr'],
                GatewayId=self.igw_id
            )
        )
    # removing a route
    def delete_route(self):
        check_response(
            ec2_client.delete_route(
                RouteTableId=self.id,
                DestinationCidrBlock=self.config['vpc']['dest-cidr']
            )
        )
    # associating the route with the route table
    def associate(self, subnet_id):
        self.subnet_id = subnet_id
        self.association_id.append(ec2_client.associate_route_table(
            RouteTableId=self.id,
            SubnetId=self.subnet_id
        )['AssociationId'])
    # diassociating the route from the route table
    def disassociate(self):
        for association_id in self.association_id:
            check_response(
                ec2_client.disassociate_route_table(
                    AssociationId=association_id
                )
            )
    # removing the route table
    def remove(self):
        check_response(
            ec2_client.delete_route_table(
                RouteTableId=self.id
            )
        )