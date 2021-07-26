# imports..
# import paillier library etc

class KeyManager():
    def __init__(self):
        # Whatever attributes are needed here...
        self.generate_keys() # Generate keys
        self.public_key = self.__read_public_key() # Read the public key and store it in the object
        self.private_key = self.__read_private_key()# Read the private key and store it in the object
        # Any other constructor logic required etc...
        pass

    def generate_keys(self):
        pass
        # Generate paillier keys
        # Write to public and private key files etc

    # In python __ in front of a method is a convention to indicate that it is a "private" method
        # In other words the method should only be used within the KeyManager class
        # and someone using the KeyManager() object should not use those methods
        # Private methods are used to indicate helper functionalities that are needed internally in the class

    def __read_public_key(self):
        pass

    def __read_public_key(self):
        # read public key
        pass

    def __write_public_key(self):
        # write public key
        pass

    def __write_private_key(self):
        pass