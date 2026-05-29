from .vars import *

class EC2:
    def __init__(self, config, prefix, kp_name, sg_id, subnet_id):
        self.config = config
        self.name = self.config['ProjectName'] + "-" + prefix + "-instance"
        self.kp_name = kp_name
        self.sg_id = sg_id
        self.subnet_id = subnet_id
        self.instance = ec2_client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 8,
                        'VolumeType': 'gp3',
                        'Encrypted': False
                    }
                },
            ],
            ImageId=self.config['ec2']['ami'],
            InstanceType='t3.micro',
            KeyName=self.kp_name,
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': False
            },
            Placement={
                'AvailabilityZone': self.config['vpc']['az']
            },
            SecurityGroupIds=[
                self.sg_id
            ],
            SubnetId=self.subnet_id,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Project',
                            'Value': self.config['ProjectName']
                        },
                    ]
                }
            ]
        )
        self.response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'reservation-id',
                    'Values': [
                        self.instance['ReservationId']
                    ]
                },
            ]
        )
        waiter = ec2_client.get_waiter('instance_exists')
        self.id = self.response['Reservations'][0]['Instances'][0]['InstanceId']
        waiter.wait(InstanceIds=[self.id])
    def remove(self):
        ec2_client.terminate_instances(
            InstanceIds=[
                self.id,
            ],
            Force=True,
            SkipOsShutdown=True
        )
        waiter = ec2_client.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=[self.id])