from .vars import *
from .checks import *

class KeyPair:
    def __init__(self, config):
        self.config = config
        self.name = self.config['ProjectName'] + "-keypair"
        self.file = None
        self.keypair = ec2_client.create_key_pair(KeyName=self.name)
        self.private_key = self.keypair['KeyMaterial']
        self.id = self.keypair['KeyMaterial']['KeyId']
    def get(self):
        self.file = open(self.config['KeyPair']['file'])
        self.file.write(self.private_key)
        self.file.close()
    def remove(self):
        check_if_true(
            ec2_client.delete_key_pair(
                KeyName=self.name,
                KeyPairId=key_id
            )
        )

def delete_keypair(name, key_id):
    response = ec2_client.delete_key_pair(KeyName=name, KeyPairId=key_id)
    check_if_true(response)
    return response