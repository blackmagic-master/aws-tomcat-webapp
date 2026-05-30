from .vars import *

class TargetGroup:
    def __init__(self, config, vpc_id):
        self.config = config
        self.name = self.config['ProjectName'].lower() + "-tg"
        self.vpc_id = vpc_id
        self.tg = elbv_client.create_target_group(
            Name=self.name,
            Protocol='HTTP',
            Port=8080,
            VpcId=self.vpc_id,
            HealthCheckProtocol='HTTP',
            HealthCheckPort='8080',
            HealthCheckEnabled=True,
            HealthCheckPath='/',
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=10,
            HealthyThresholdCount=3,
            UnhealthyThresholdCount=2,
            Matcher={
                'HttpCode': '200'
            },
            TargetType='instance',
            Tags=[
                {
                    'Key': 'Project',
                    'Value': self.config['ProjectName']
                },
            ],
            IpAddressType='ipv4'        )
        self.arn = self.tg['TargetGroups'][0]['TargetGroupArn']
    def register_targets(self, ec2_id):
        elbv_client.register_targets(
            TargetGroupArn=self.arn,
            Targets=[
                {
                    'Id': ec2_id,
                    'Port': 8080
                }
            ]
        )
    def deregister_targets(self, ec2_id):
        elbv_client.deregister_targets(
            TargetGroupArn=self.arn,
            Targets=[
                {
                    'Id': ec2_id,
                    'Port': 8080
                }
            ]
        )
    def remove(self):
        elbv_client.delete_target_group(
            TargetGroupArn=self.arn
        )