# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 12:31:26 2021

@author: Garret_H
"""
import pickle
from newer_gabes.yao import encrypt
from newer_gabes.wire import Wire
from newer_gabes.gate import Gate
from cryptography.fernet import Fernet, InvalidToken
from Crypto.Random.random import shuffle

class GarbledGate(Gate):
    """A representation of a garbled gate.

    Args:
        gate: A dict containing gate spec.
        keys: A dict mapping each wire to a pair of keys.
        pbits: A dict mapping each wire to its p-bit.
    """
    def __init__(self, gate, keys):
        self.keys = keys  # dict of yao circuit keys
        self.input = [Wire(str(x)) for x in gate['in']]  # list of inputs'ID
        self.output = Wire(str(gate['id']))  # ID of output
        self.gate_type = gate["type"]  # Gate type: OR, AND, ...
        self.garbled_table = {}  # The garbled table of the gate
        self.chosen_label = None
        # A clear representation of the garbled table for debugging purposes
        self.clear_garbled_table = {}
        self.table = []

        # Create the garbled table according to the gate type
        # switch = {
        #     "OR": lambda b1, b2: b1 or b2,
        #     "AND": lambda b1, b2: b1 and b2,
        #     "XOR": lambda b1, b2: b1 ^ b2,
        #     "NOR": lambda b1, b2: not (b1 or b2),
        #     "NAND": lambda b1, b2: not (b1 and b2),
        #     "XNOR": lambda b1, b2: not (b1 ^ b2)
        # }

        # NOT gate is a special case since it has only one input
        # if (self.gate_type == "NOT"):
        #     self._gen_garbled_table_not()
        # else:
        #     operator = switch[self.gate_type]
        #     self._gen_garbled_table(operator)

    def _gen_garbled_table_not(self):
        """Create the garbled table of a NOT gate."""
        inp, out = self.input[0], self.output

        # For each entry in the garbled table
        for encr_bit_in in (0, 1):
            # Retrieve original bit
            bit_in = encr_bit_in ^ self.pbits[inp]
            # Compute output bit according to the gate type
            bit_out = int(not (bit_in))
            # Compute encrypted bit with the p-bit table
            encr_bit_out = bit_out ^ self.pbits[out]
            # Retrieve related keys
            key_in = self.keys[inp][bit_in]
            key_out = self.keys[out][bit_out]

            # Serialize the output key along with the encrypted bit
            msg = pickle.dumps((key_out, encr_bit_out))
            # Encrypt message and add it to the garbled table
            self.garbled_table[(encr_bit_in, )] = encrypt(key_in, msg)
            # Add to the clear table indexes of each keys
            self.clear_garbled_table[(encr_bit_in, )] = [(inp, bit_in),
                                                         (out, bit_out),
                                                         encr_bit_out]

    def _gen_garbled_table(self, operator):
        """Create the garbled table of a 2-input gate.

        Args:
            operator: The logical function of to the 2-input gate type.
        """
        in_a, in_b, out = self.input[0], self.input[1], self.output

        # Same model as for the NOT gate except for 2 inputs instead of 1
        for encr_bit_a in (0, 1):
            for encr_bit_b in (0, 1):
                bit_a = encr_bit_a ^ self.pbits[in_a]
                bit_b = encr_bit_b ^ self.pbits[in_b]
                bit_out = int(operator(bit_a, bit_b))
                encr_bit_out = bit_out ^ self.pbits[out]
                key_a = self.keys[in_a][bit_a]
                key_b = self.keys[in_b][bit_b]
                key_out = self.keys[out][bit_out]

                msg = pickle.dumps((key_out, encr_bit_out))
                self.garbled_table[(encr_bit_a, encr_bit_b)] = encrypt(
                    key_a, encrypt(key_b, msg))
                self.clear_garbled_table[(encr_bit_a, encr_bit_b)] = [
                    (in_a, bit_a), (in_b, bit_b), (out, bit_out), encr_bit_out
                ]

    def print_garbled_table(self):
        """Print a clear representation of the garbled table."""
        print(f"GATE: {self.output}, TYPE: {self.gate_type}")
        for k, v in self.clear_garbled_table.items():
            # If it's a 2-input gate
            if len(k) > 1:
                key_a, key_b, key_out = v[0], v[1], v[2]
                encr_bit_out = v[3]
                print(f"[{k[0]}, {k[1]}]: "
                      f"[{key_a[0]}, {key_a[1]}][{key_b[0]}, {key_b[1]}]"
                      f"([{key_out[0]}, {key_out[1]}], {encr_bit_out})")
            # Else it's a NOT gate
            else:
                key_in, key_out = v[0], v[1]
                encr_bit_out = v[2]
                print(f"[{k[0]}]: "
                      f"[{key_in[0]}, {key_in[1]}]"
                      f"([{key_out[0]}, {key_out[1]}], {encr_bit_out})")

    def get_garbled_table(self):
        """Return the garbled table of the gate."""
        return self.garbled_table
    def is_output(self, circ):
        for other in circ.gates:
            if self.output in other.input:
                return False
        return True
    
    def is_input(self, circ):
        for other in circ.gates:
            if (self.input[0] or self.input[1]) is other.output:
                return False
        return True

    def garble(self):

        check = []
        for label1 in self.input[0].labels():
            for label2 in self.input[1].labels():
                key1 = Fernet(label1.to_base64())
                key2 = Fernet(label2.to_base64())
                in1, in2 = label1.represents, label2.represents
                logic_value = self.evaluate_gate(in1, in2)
                output_label = self.output.get_label(logic_value)
                pickled = pickle.dumps(output_label)
                table_entry = key1.encrypt(key2.encrypt(pickled))
                self.table.append(table_entry)
                check.append(str(label1)[:4] + ' ' + str(label2)[:4])
        print(check)

        shuffle(self.table)

    def ungarble(self, garblers_label, evaluators_label):
        print(garblers_label)
        print(evaluators_label)
        for table_entry in self.table:
            try:
                key2 = Fernet(garblers_label.to_base64())
                key1 = Fernet(evaluators_label.to_base64())
                output_label = pickle.loads(key1.decrypt(key2.decrypt(table_entry)))
            except InvalidToken:
                # Wrong table entry, try again
                pass
        return output_label