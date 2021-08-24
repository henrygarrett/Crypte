import pickle
from random import randint
from newer_gabes.garbler import Alice

class Bob():
    def __init__(self):
        self.__chosen_bit = None
        self.__k = None
        self.__inputs = {'3': 1, '4': 1}

        
    def main(self):
        alice = Alice()
        identifiers = alice.start()
        labels = self.request_labels(identifiers, self.__inputs, alice)
        circ = alice.hand_over_cleaned_circuit()
        secret_output = circ.reconstruct(labels)
        final_output = alice.learn_output(secret_output)
        print("The final output of the circuit is: {}".format(final_output))
        return final_output
    

    def request_labels(self, identifiers, evaluator_inputs, alice):
        labels = []
        if not set(evaluator_inputs.keys()).issubset(set(identifiers)):
            raise ValueError('You have supplied a wire identifier not in the circuit.')
        for identifier in identifiers:
            if identifier in evaluator_inputs:
                self.__chosen_bit = evaluator_inputs[identifier]
                alice.set_labels(identifier)
                x0, x1, n, e = alice.garbot1()
                w = self.evalot1(x0, x1, n, e)
                t0, t1, size_m0, size_m1 = alice.garbot2(w, x0, x1, n)
                secret_label = self.evalot2(t0, t1, size_m0, size_m1)
            else:
                secret_label = alice.send_label(identifier)
            labels.append(secret_label)
        return labels
 

    def evalot1(self, x0, x1, n, e):
        b =  self.__chosen_bit
        k = randint(2, n // 2)
        chosen_x = x1 if b == '1' else x0
        w = (chosen_x + pow(k, e, n)) % n
        self.__k = k
        return w


    def evalot2(self, t0, t1, size_m0, size_m1):
        b = self.__chosen_bit
        chosen_t = t1 if b == '1' else t0
        chosen_size = size_m1 if b == '1' else size_m0
        m = chosen_t - self.__k
        label = pickle.loads(int.to_bytes(m, length=chosen_size, byteorder='big'))
        return label
