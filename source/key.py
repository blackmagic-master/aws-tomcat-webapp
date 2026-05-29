from .vars import *
from .checks import *

class KeyPair:
    def __init__(self, config):
        self.config = config
        self.name = self.config['ProjectName'] + "-keypair"
        self.file = None
        self.keypair = ec2_client.create_key_pair(KeyName=self.name)
        self.private_key = self.keypair['KeyMaterial']
        self.id = self.keypair['KeyPairId']
    def get(self):
        self.file = open(self.config['KeyPair']['file'], 'w')
        self.file.write(self.private_key)
        self.file.close()
    def remove(self):
        check_if_true(
            ec2_client.delete_key_pair(
                KeyName=self.name,
                KeyPairId=self.id
            )
        )