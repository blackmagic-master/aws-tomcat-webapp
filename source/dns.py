from .vars import *
import uuid

class HostedZone:
    def __init__(self, config, vpc_id):
        self.config = config
        self.name = self.config['ProjectName'].lower() + ".hz"
        self.az = self.config['vpc']['az'][0:len(self.config['vpc']['az'])-1]
        self.vpc_id = vpc_id
        hz = route53_client.create_hosted_zone(
            Name=self.name,
            VPC={
                'VPCRegion': self.az,
                'VPCId': self.vpc_id
            },
            CallerReference=str(uuid.uuid4()),
            HostedZoneConfig={
                'PrivateZone': False
            }
        )
        self.id = hz['HostedZone']['Id']
    def add_a_record(self, dns_name, ip):
        route53_client.change_resource_record_sets(
            ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'CREATE',
                            'ResourceRecordSet': {
                                'Name': dns_name + "." + self.name,
                                'ResourceRecords': [
                                    {
                                        'Value': ip,
                                    },
                                ],
                                'TTL': 60,
                                'Type': 'A',
                            },
                        },
                    ],
                    'Comment': 'Web server for example.com',
                },
                HostedZoneId=self.id,
            )
    def remove(self):
        route53_client.delete_hosted_zone(
            Id=self.id
        )