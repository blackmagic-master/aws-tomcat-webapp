from .vars import *

class LoadBalancer:
    def __init__(self, config, subnets, sg_id):
        self.config = config
        self.name = self.config['ProjectName'].lower() + "-lb"
        self.subnets = subnets
        self.sg_id = sg_id
        self.listener_arn = None
        self.lb = elbv_client.create_load_balancer(
            Name=self.name,
            Subnets=subnets,
            SecurityGroups=[
                self.sg_id
            ],
            Scheme='internet-facing',
            Tags=[
                {
                    'Key': 'Project',
                    'Value': self.config['ProjectName']
                },
            ],
            Type='application',
            IpAddressType='ipv4'
        )
        self.arn = self.lb['LoadBalancers'][0]['LoadBalancerArn']
        self.dns_name = self.lb['LoadBalancers'][0]['DNSName']
    def create_listener(self, tg_arn):
        listener = elbv_client.create_listener(
            DefaultActions=[
                {
                    'TargetGroupArn': tg_arn,
                    'Type': 'forward',
                },
            ],
            LoadBalancerArn=self.arn,
            Port=80,
            Protocol='HTTP'
        )
        self.listener_arn = listener['Listeners'][0]['ListenerArn']
    def delete_listener(self):
        elbv_client.delete_listener(
            ListenerArn=self.listener_arn,
        )
    def remove(self):
        elbv_client.delete_load_balancer(
            LoadBalancerArn=self.arn
        )