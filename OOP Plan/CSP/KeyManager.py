# imports..
# import paillier library etc
import pathlib
import sys
import pickle
path = str(pathlib.Path.cwd().parents[0])
sys.path.append(path + '\\Lab Paillier')
from lab_paillier import generate_lab_paillier_keypair
class KeyManager():
    def __init__(self, new):
        if new:
            self.generate_keys()
        else:
            self.public_key = self.__read_public_key()
            self.private_key = self.__read_private_key()
        

    def generate_keys(self):
        public_key, private_key = generate_lab_paillier_keypair()
        self.__write_public_key(public_key)
        self.__write_private_key(private_key)
        self.public_key = public_key
        self.private_key = private_key

    def __read_public_key(self):
        with open(path + '\\Public Key\\public_key', 'rb') as public_key_file:
            return pickle.load(public_key_file)

    def __read_private_key(self):
        with open(path + '\\CSP\\private_key', 'rb') as private_key_file:
            return pickle.load(private_key_file)

    def __write_public_key(self, public_key):
        with open(path + '\\Public Key\\public_key', 'wb') as public_key_file:
            pickle.dump(public_key, public_key_file)

    def __write_private_key(self, private_key):
        with open(path + '\\CSP\\private_key', 'wb') as private_key_file:
            pickle.dump(private_key, private_key_file)
