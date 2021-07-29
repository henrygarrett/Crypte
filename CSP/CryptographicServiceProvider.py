from pathlib import Path
path = str(Path.cwd().parents[2])#index needs to be set for cwd which will likely be where operators are run not this file

from .PrivacyEngine import PrivacyEngine
from .KeyManager import KeyManager
from .DataDecryption import DataDecryption


class CryptographicServiceProvider():
    def __init__(self, epsilon_budget, generate_keys=False):
        self.privacy_engine = PrivacyEngine(epsilon_budget)
        self.key_manager = KeyManager(generate_keys)
        self.data_decryption = DataDecryption()