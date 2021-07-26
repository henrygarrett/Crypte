import pickle
import os
import ast
import random
import gmpy2
 

#imports public key to encrypt DOs data 
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Public_Key\\public_key', 'rb') as public_key_file:
    public_key = pickle.load(public_key_file)
 
with open('data_set.txt', 'r') as data_set_file:
    data_set = ast.literal_eval(data_set_file.read())


def localGen(pk):
    seed = ''
    for i in range(100):
        seed += str(random.randint(0,1))
    seed_encoded = int(seed,2)
    seed_encrypted = pk.encrypt(seed_encoded, None)
    print(seed_encrypted)
    return bin(seed_encoded), seed_encrypted
def gen_label():
    label = str(random.randint(0,9))
    for i in range(29):
        label += str(random.randint(0,9))
    return int(label)

for data in data_set:
    
    countries = ['uk', 'france', 'germany', 'spain', 'italy']
    data_onehot_encoded = []
    age_onehot_encoded = [0 for i in range(20,41)]
    age_onehot_encoded[int(data[0])-20] = 1#puts a 1 at the age-th position
    smoke_onehot_encoded = [1,0] if data[2] == 'yes' else [0,1]
    country_onehot_encoded = [0 for i in range(len(countries))]
    country_onehot_encoded[int(countries.index(data[1]))] = 1
    data_onehot_encoded.append(age_onehot_encoded)
    data_onehot_encoded.append(country_onehot_encoded)
    data_onehot_encoded.append(smoke_onehot_encoded)
    print(data_onehot_encoded)
    seed, pki = localGen(public_key)
    label = gen_label()

    data_encrypted = [[public_key.lab_encrypt(value, label, seed) for value in attribute] for attribute in data_onehot_encoded]
    print(data_encrypted)
    path, dirs, files = next(os.walk('C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Aggregator\\Raw Data'))
    file_count = len(files)
    print(file_count)
    with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Aggregator\\Raw Data\\data_' + str(file_count) , 'wb') as data_file:
      pickle.dump(data_encrypted, data_file)