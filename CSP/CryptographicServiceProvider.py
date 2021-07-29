from pathlib import Path
path = str(Path.cwd().parents[2])#index needs to be set for cwd which will likely be where operators are run not this file

from .PrivacyEngine import PrivacyEngine
from .KeyManager import KeyManager
from .DataDecryption import DataDecryption

import sys
sys.path.append(path + '\\Crypte\\Lab paillier')

class CryptographicServiceProvider():
    def __init__(self, epsilon_budget, new):
        self.privacy_engine = PrivacyEngine(epsilon_budget)
        self.key_manager = KeyManager(new)
        self.data_decryption = DataDecryption()

    def lab_mult(self):
        out = self.data_decryption.lab_multiplication(self.key_manager.public_key, self.key_manager.private_key, )
        return out