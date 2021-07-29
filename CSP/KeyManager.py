import pathlib
import pandas as pd
import os

from lab_paillier.lab_paillier import LabPaillierPublicKey, LabPaillierPrivateKey, generate_lab_paillier_keypair

PATH = str(pathlib.Path.cwd().parents[0])
PUBLIC_KEY_PATH = PATH + os.sep + 'public_key' + os.sep + 'public_key.csv'
PRIVATE_KEY_PATH = PATH + os.sep + 'CSP' + os.sep + 'private_key.csv'

class KeyManager():
    def __init__(self, generate_keys=False):
        if generate_keys:
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
        df = pd.read_csv(PUBLIC_KEY_PATH)
        return LabPaillierPublicKey(int(df['n'].values[0]))

    def __read_private_key(self):
        df = pd.read_csv(PRIVATE_KEY_PATH)
        return LabPaillierPrivateKey(self.public_key, int(df['p'].values[0]), int(df['q'].values[0]))

    def __write_public_key(self, public_key):
        df = pd.DataFrame({'n': str(public_key.n)}, index=[0])
        df.to_csv(PUBLIC_KEY_PATH, index=False)

    def __write_private_key(self, private_key):
        df = pd.DataFrame({'p': str(private_key.p), 'q': str(private_key.q)}, index=[0])
        df.to_csv(PRIVATE_KEY_PATH, index=False)
