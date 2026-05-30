from .vars import *

class EC2:
    def __init__(self, config, prefix, kp_name, sg_id, subnet_id, dns_name):
        self.config = config
        self.dns_name = dns_name
        self.name = self.config['ProjectName'] + "-" + prefix + "-instance"
        self.kp_name = kp_name
        self.sg_id = sg_id
        self.subnet_id = subnet_id
        self.userdata = scripts[prefix]
        self.ami = None
        if prefix == 'TOMCAT':
            self.ami = self.config['Ec2']['TomcatAmi']
        else:
            self.ami = self.config['Ec2']['BackendAmi']
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
            ImageId=self.ami,
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
            UserData=self.userdata,
            SubnetId=self.subnet_id,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Project',
                            'Value': self.config['ProjectName']
                        },
                        {
                            'Key': 'Name',
                            'Value': self.name
                        }
                    ]
                }
            ]
        )
        self.response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        self.name
                    ]
                },
                {
                    'Name': 'subnet-id',
                    'Values': [
                        self.subnet_id
                    ]
                },
            ]
        )
        waiter = ec2_client.get_waiter('instance_running')
        self.id = self.response['Reservations'][0]['Instances'][0]['InstanceId']
        waiter.wait(InstanceIds=[self.id])
        self.private_ip = self.response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress']
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