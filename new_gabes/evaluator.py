"""
    This module provides the communication protocol seen from the point
    of view of the evaluator. To learn the whole process,
    see the Garbler's section.
"""
import pickle
import new_gabes.network as net

from new_gabes.ot import evaluator_ot
from new_gabes.utils import ask_for_inputs


def evaluator():
    """
        The main function of the application for the evaluator. For
        more information on the process, see the introduction to
        the Garbler's section.


        :param args: the arguments from the command line interface
        :return: the output of the circuit
        :rtype: bool

    """
    print("Welcome, evaluator. Waiting for the garbler...")
    idents = request_wire_identifiers()
    # if args.identifiers:
    #     inputs = {x: y for x, y in zip(args.identifiers, args.bits)}
    # else:
    #     inputs = ask_for_inputs(idents)
    inputs = {'4':1,'5':0,'6':0}
    labels = request_labels(idents, inputs)
    circ = request_cleaned_circuit()
    print("Reconstructing circuit...")
    secret_output = circ.reconstruct(labels)
    name = '1066'
    with open('send_data' + name, 'w') as file:
            file.write(1)
    final_output = learn_output(name, secret_output)
    print("The final output of the circuit is: {}".format(final_output))
    return final_output


def request_wire_identifiers():
    """
        Receives the wire identifiers from the garbler.

        :param sock: the socket from which it will receive the data
        :return: the identifiers of the input wires
        :rtype: list(str)

    """
    with open('hand_over_wire_identifiers.txt', 'r') as file:
        identifiers = file.read()
    return identifiers


def request_cleaned_circuit():
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


def request_labels(identifiers, evaluator_inputs):
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
            chosen_bit = evaluator_inputs[identifier]
            secret_label = evaluator_ot(chosen_bit)
        else:
            with open('hand_over_labels', 'rb') as file:
                secret_label = pickle.load(file)
        labels.append(secret_label)
    return labels


def learn_output(name, secret_output):
    """
        Sends the final label and learns the final truth value
        from the garbler.

        :param sock: the socket from which it will receive the data
        :param secret_output: the final label of the circuit
        :return: the output of the circuit
        :rtype: bool

    """
    net.send_data(secret_output)
    final_output = net.receive_data(name)
    return final_output
