# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 12:30:23 2021

@author: Garret_H
"""
from cryptography.fernet import Fernet
from newer_gabes.garbledgate import GarbledGate
import copy
class GarbledCircuit:
    """A representation of a garbled circuit.

    Args:
        circuit: A dict containing circuit spec.
        pbits: Optional; a dict of p-bits for the given circuit.
    """
    def __init__(self, circuit):
        self.circuit = circuit
        self.wires = [] # list of circuit wires
        self.input_wires = []
        self.keys = {}  # dict of keys
        self.garbled_tables = {}  # dict of garbled tables

        # Retrieve all wire IDs from the circuit
        
        self._gen_keys()
        
        self.gates = [GarbledGate(gate, self.keys) for gate in circuit["gates"]]  # list of gates
        self.output_gates = [gate for gate in self.gates if gate.is_output(self)]
        for gate in self.gates:
            self.wires.append(gate.output)
            self.wires.extend(gate.input)
        temp_list = []
        for wire in self.wires:
            if wire.identifier not in [item.identifier for item in temp_list]:
                temp_list.append(wire)
        self.wires = temp_list
        self._gen_garbled_tables()

    def _gen_keys(self):
        """Create pair of keys for each wire."""
        for wire in self.wires:
            self.keys[wire.identifier] = (Fernet.generate_key(), Fernet.generate_key())

    def _gen_garbled_tables(self):
        """Create the garbled table of each gate."""
        for gate in self.gates:
            self.garbled_tables[gate.output.identifier] = gate.get_garbled_table()

    def print_garbled_tables(self):
        """Print p-bits and a clear representation of all garbled tables."""
        print(f"======== {self.circuit['id']} ========")
        print(f"P-BITS: {self.pbits}")
        for gate in self.gates:
            garbled_table = GarbledGate(gate, self.keys)
            garbled_table.print_garbled_table()
        print()

    def get_pbits(self):
        """Return dict mapping each wire to its p-bit."""
        return self.pbits

    def get_garbled_tables(self):
        """Return dict mapping each gate to its garbled table."""
        return self.garbled_tables

    def get_keys(self):
        """Return dict mapping each wire to its pair of keys."""
        return self.keys
    
    def get_input_wires(self):
        if self.input_wires == []:
            for wire in self.wires:
                if wire not in [gate.output for gate in self.gates]:
                    self.input_wires.append(wire)
        return self.input_wires
    def clean(self):
        circ = copy.deepcopy(self)
        for gate in self.gates:
            gate.garble()
            gate.input = gate.output = None
        return circ
    
    
    def reconstruct(self, labels):
        """
            Function used by the evaluator to reconstruct the circuit given
            only the input labels by the garbler. The reconstruction needs
            to be done in a bottom-up approach since the output labels of
            input gates will serve as input labels for parent gates.
            The function traverses the tree by level starting at the leaves.
            If the nodes are leaves, then the labels will be provided through
            the network by the garbler. For all other nodes, the evaluator will
            have the necessary labels as part of the node's children by a
            process of ungarbling (see :meth:`gabes.gate.Gate.ungarble`).

            :param labels: the list of input labels supplied by the garbler
            :type labels: list(:class:`Label`)
            :return: the final output label at the end of the circuit
            :rtype: :class:`Label`

        """
        for gate in self.gates:
            print(gate)
            self.chosen_label(gate, labels)
                
                
                
        return [gate.chosen_label for gate in self.output_gates]
    def chosen_label(self, gate, labels):
                if gate.is_input(self):
                    print(labels)
                    evaluators_label = labels.pop(0)
                    garblers_label = labels.pop(0)
                else:
                    print('input type: ' + str(type(gate.input[0])))
                    garblers_label = self.chosen_label(gate.input[1], labels)
                    evaluators_label = self.chosen_label(gate.input[0],labels)
                output_label = gate.ungarble(garblers_label, evaluators_label)
                gate.chosen_label = output_label
                return gate.chosen_label
    
    
    






