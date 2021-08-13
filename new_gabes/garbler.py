"""
    This module provides the communication protocol seen from the point
    of view of the garbler. First, the garbler and the evaluator establish
    a connection through a socket. Then the garbler creates the circuit
    and garbles all the gates. He then sends to the evaluator
    the wire identifiers so that the evaluator can choose which truth
    values to supply to each wire he controls. After this,
    the input labels are transferred to the evaluator.
    Following the garbled circuits protocol, the garbler's labels can be
    sent *as is*, as they are obfuscated so the evaluator can not learn
    anything. The evaluator's labels however are trickier,
    so a 1-out-of-2 oblivious transfer protocol must be followed
    for each input label the evaluator supplies.

    Once the evaluator is in possesion of all the input labels,
    he can reconstruct the circuit and send the final output label
    to the garbler. The garbler can then compare the label in his
    circuit and decide which truth value it corresponds.
    Finally, the garbler sends the evaluator the final truth value.

"""
import copy
import pickle
import new_gabes.network as net

from new_gabes.circuit import Circuit
from new_gabes.utils import ask_for_inputs
from new_gabes.ot import garbler_ot
from new_gabes.label import Label

def garbler(circ):
    """
        The main function of the application for the garbler. For
        more information on the process, see above.


        :param args: the arguments from the command line interface
        :return: the output of the circuit
        :rtype: bool

    """
    print("Welcome, garbler. Waiting for the evaluator...")
    circ = Circuit(circ)
    print("Circuit created...")
    identifiers = hand_over_wire_identifiers(circ)
    print(identifiers)
    #if circ.identifiers:
        #inputs = [{x: y for x, y in zip(circ.identifiers, args.bits)}]
    #else:
    #inputs = ask_for_inputs(identifiers)
    #print(inputs)
    inputs = {'1':0, '2':1,'3':1}
    hand_over_labels(circ, inputs)
    hand_over_cleaned_circuit(circ)
    name = '1066'
    with open('send_data' + name, 'wb') as data_file:
            pickle.dump(Label(1),data_file)
    final_output = learn_output(name, circ)
    print("The final output of the circuit is: {}".format(final_output))
    return final_output


def hand_over_wire_identifiers(circ):
    """
        Sends the wire identifiers to the evaluator.

        :param client: the client is the evaluator
        :param circ: the circuit to which the wires belong
        :return: the identifiers of the input wires
        :rtype: list(str)

    """
    identifiers = [wire.identifier for wire in circ.get_input_wires()]
    with open('hand_over_wire_identifiers.txt', 'w') as data_set_file:
                data_set_file.write(str(identifiers))
    return identifiers


def hand_over_cleaned_circuit(circ):
    """
        Sends a clean circuit (in which every label's *represents*
        flag has been deleted) to the evaluator.

        :param client: the client is the evaluator
        :param circ: the circuit in question

    """
    new_circ = circ.clean()
    with open('hand_over_cleaned_circuit', 'wb') as data_file:
            pickle.dump(new_circ, data_file)


def hand_over_labels(circ, garbler_inputs):
    """
        Sends the input labels of the circuit to the evaluator. The labels
        that belong to the garbler can be sent without any modification.
        In order for the evaluator to learn his labels, he must acquire
        them through the oblivious transfer protocol, in which the
        garbler inputs the two possible labels, the evaluator inputs
        his choice of truth value, and the evaluator learns which
        label corresponds to his truth value without the garbler learning
        his choice and without the evaluator learning both labels.

        :param client: the client is the evaluator
        :param circ: the circuit in question
        :param garbler_inputs: the inputs the garbler provides

    """
    identifiers = set(wire.identifier for wire in circ.get_input_wires())
    if not set(garbler_inputs.keys()).issubset(set(identifiers)):
        raise ValueError('You have supplied a wire '
                         'identifier not in the circuit.')
    for wire in circ.get_input_wires():
        if wire.identifier in garbler_inputs:
            chosen_bit = garbler_inputs[wire.identifier]
            if chosen_bit == '1':
                secret_label = wire.true_label
            else:
                secret_label = wire.false_label
                
            with open('hand_over_labels', 'wb') as file:
                pickle.dump(secret_label, file)
            net.send_data('secret_label',secret_label)
            #net.wait_for_ack(client)
        else:
            false_label = copy.deepcopy(wire.false_label)
            true_label = copy.deepcopy(wire.true_label)
            # Clean before sending
            false_label.represents = true_label.represents = None
            garbler_ot(false_label, true_label)


def learn_output(name, circ):
    """
        Learns the final truth value of the circuit by comparing the label that
        was handed to him by the evaluator to the two labels in the root of the
        tree (i.e. the final gate).

        :param client: the client is the evaluator
        :param circ: the circuit in question
        :return: the output of the circuit
        :rtype: bool

    """
    output_label = net.receive_data(name)
    output_gate = circ.tree.name
    out1 = output_gate.output_wire.true_label.to_base64()
    out2 = output_label.to_base64()
    output = out1 == out2
    net.send_data('output',output)
    return output
