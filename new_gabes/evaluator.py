"""
    This module provides the communication protocol seen from the point
    of view of the evaluator. To learn the whole process,
    see the Garbler's section.
"""
import pickle
from new_gabes.utils import ask_for_inputs
from random import randint
from new_gabes.garbler import Alice
class Bob():
    def __init__(self):
        self.__chosen_bit = None
        self.__k = None
    def bob(self, inputs=None):
        """
            The main function of the application for the evaluator. For
            more information on the process, see the introduction to
            the Garbler's section.
    
    
            :param args: the arguments from the command line interface
            :return: the output of the circuit
            :rtype: bool
    
        """
        alice = Alice()
        identifiers = alice.alice1()
        if inputs == None:
            inputs = ask_for_inputs(identifiers)
        else:
            inputs = inputs
        labels = self.request_labels(identifiers, inputs, alice)
        circ = alice.alice2()
        secret_output = circ.reconstruct(labels)
        final_output = alice.alice3(secret_output)
        print("The final output of the circuit is: {}".format(final_output))
        return final_output
    
    
    def request_wire_identifiers(self):
        """
            Receives the wire identifiers from the garbler.
    
            :param sock: the socket from which it will receive the data
            :return: the identifiers of the input wires
            :rtype: list(str)
    
        """
        with open('hand_over_wire_identifiers.txt', 'r') as file:
            identifiers = file.read()
        return identifiers
    
    
    def request_cleaned_circuit(self):
        """
            Receives a clean circuit (in which every label's *represents*
            flag has been deleted) from the garbler.
    
            :param sock: the socket from which it will receive the data
            :return: the cleaned circuit
            :rtype: :class:`Circuit`
    
        """
        with open('hand_over_cleaned_circuit', 'rb') as file:
            circuit = pickle.load(file)
        return circuit
    
    def request_labels(self, identifiers, evaluator_inputs, alice):
        """
            Receives the input labels of the circuit from the garbler. The labels
            that belong to the garbler can be sent without any modification.
            In order for the evaluator to learn his labels, he must acquire
            them through the oblivious transfer protocol, in which the
            garbler inputs the two possible labels, the evaluator inputs
            his choice of truth value, and the evaluator learns which
            label corresponds to his truth value without the garbler learning
            his choice and without the evaluator learning both labels.
    
            :param sock: the socket from which it will receive the data
            :param identifiers: the identifiers for all the input wires
            :param evaluator_inputs: the inputs the evaluator provides
            :return: the input labels
            :rtype: list(:class:`Label`)
    
        """
        labels = []
        if not set(evaluator_inputs.keys()).issubset(set(identifiers)):
            raise ValueError('You have supplied a wire '
                             'identifier not in the circuit.')
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
