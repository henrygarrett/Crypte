#!/usr/bin/env python3
import hashlib
import logging
import pickle

from garbled_circuits import yao, util
from abc import ABC, abstractmethod

logging.basicConfig(format="[%(levelname)s] %(message)s",
                    level=logging.WARNING)

# Base class for Alice garbler
class YaoGarbler(ABC):
    """An abstract class for Yao garblers (e.g. Alice)."""
    def __init__(self, circuits):
        circuits = util.parse_json(circuits)
        self.name = circuits["name"]
        self.circuits = []

        for circuit in circuits["circuits"]:
            garbled_circuit = yao.GarbledCircuit(circuit)
            pbits = garbled_circuit.get_pbits()
            entry = {
                "circuit": circuit,
                "garbled_circuit": garbled_circuit,
                "garbled_tables": garbled_circuit.get_garbled_tables(),
                "keys": garbled_circuit.get_keys(),
                "pbits": pbits,
                "pbits_out": {w: pbits[w]
                              for w in circuit["out"]},
            }
            self.circuits.append(entry)


class Alice(YaoGarbler):
    """Alice is the creator of the Yao circuit.

    Alice creates a Yao circuit and sends it to the evaluator along with her
    encrypted inputs. Alice will finally print the truth table of the circuit
    for all combination of Alice-Bob inputs.

    Alice does not know Bob's inputs but for the purpose
    of printing the truth table only, Alice assumes that Bob's inputs follow
    a specific order.

    Attributes:
        circuits: the JSON file containing circuits
        oblivious_transfer: Optional; enable the Oblivious Transfer protocol
            (True by default).
    """
    def __init__(self, input, circuits):
        super().__init__(circuits)
        self.input = input
        self.garbled_circuits = []
        self.G = None
        self.c = None

    @staticmethod
    def ot_hash(pub_key, msg_length):
        """Hash function for OT keys."""
        key_length = (pub_key.bit_length() + 7) // 8  # key length in bytes
        bytes = pub_key.to_bytes(key_length, byteorder="big")
        return hashlib.shake_256(bytes).digest(msg_length)

    def ot_send(self):
        self.G = util.PrimeGroup()
        self.c = self.G.gen_pow(self.G.rand_int())
        return self.G,self.c

    def ot_receive(self, w, h0):
        h1 = self.G.mul(self.c, self.G.inv(h0))
        k = self.G.rand_int()
        c1 = self.G.gen_pow(k)

        msgs = pickle.dumps(self.b_keys[w][0]), pickle.dumps(self.b_keys[w][1])

        e0 = util.xor_bytes(msgs[0], self.ot_hash(self.G.pow(h0, k), len(msgs[0])))
        e1 = util.xor_bytes(msgs[1], self.ot_hash(self.G.pow(h1, k), len(msgs[1])))

        return c1, e0, e1

    def garble_circuits(self):
        """Start Yao protocol."""
        for i,circuit in enumerate(self.circuits):
            to_send = {
                "circuit": circuit["circuit"],
                "garbled_tables": circuit["garbled_tables"],
                "pbits_out": circuit["pbits_out"],
            }
            logging.debug(f"Sending {circuit['circuit']['id']}")
            self.garbled_circuits.append(to_send)

    def send_inputs(self):
        """Print circuit evaluation for all Bob and Alice inputs.

        Args:
            entry: A dict representing the circuit to evaluate.
        """
        entry = self.circuits[0]
        circuit, pbits, keys = entry["circuit"], entry["pbits"], entry["keys"]
        outputs = circuit["out"]
        a_wires = circuit.get("alice", [])  # Alice's wires
        a_inputs = {}  # map from Alice's wires to (key, encr_bit) inputs
        b_wires = circuit.get("bob", [])  # Bob's wires
        b_keys = {  # map from Bob's wires to a pair (key, encr_bit)
            w: self._get_encr_bits(pbits[w], key0, key1)
            for w, (key0, key1) in keys.items() if w in b_wires
        }

        self.b_keys = b_keys # Store b_keys for later OT computations

        print(f"======== Circuit ID: {circuit['id']} ========")

        bits_a = self.input  # Alice's inputs

        # Map Alice's wires to (key, encr_bit)
        for i in range(len(a_wires)):
            a_inputs[a_wires[i]] = (keys[a_wires[i]][bits_a[i]],
                                    pbits[a_wires[i]] ^ bits_a[i])

        # Send Alice's encrypted inputs and keys to Bob
        return a_inputs


    def _get_encr_bits(self, pbit, key0, key1):
        return ((key0, 0 ^ pbit), (key1, 1 ^ pbit))


class Bob:
    """Bob is the receiver and evaluator of the Yao circuit.

    Bob receives the Yao circuit from Alice, computes the results and sends
    them back.

    Args:
        oblivious_transfer: Optional; enable the Oblivious Transfer protocol
            (True by default).
    """
    def __init__(self, input):
        self.input = input

        # First half of OT params sent by Alice
        self.G = None
        self.c = None

    @staticmethod
    def ot_hash(pub_key, msg_length):
        """Hash function for OT keys."""
        key_length = (pub_key.bit_length() + 7) // 8  # key length in bytes
        bytes = pub_key.to_bytes(key_length, byteorder="big")
        return hashlib.shake_256(bytes).digest(msg_length)

    def ot_send(self, b, G, c):
        self.G = G
        self.c = c

        self.x = self.G.rand_int()
        x_pow = self.G.gen_pow(self.x)
        h = (x_pow, self.G.mul(self.c, self.G.inv(x_pow)))

        return h[b] # h0 for alice

    def ot_receive(self, b, c1, e0, e1):
        e = (e0, e1)
        ot_hash = self.ot_hash(self.G.pow(c1, self.x), len(e[b]))
        mb = util.xor_bytes(e[b], ot_hash)
        return mb

    def receive_circuits_and_inputs(self, entry, a_inputs):
        """Evaluate yao circuit for all Bob and Alice's inputs and
        send back the results.

        Args:
            entry: A dict representing the circuit to evaluate.
        """
        # Store garbled circuits and pbits to use during evaluation later
        self.circuit, self.pbits_out = entry["circuit"], entry["pbits_out"]
        self.garbled_tables = entry["garbled_tables"]

        a_wires = self.circuit.get("alice", [])  # list of Alice's wires
        b_wires = self.circuit.get("bob", [])  # list of Bob's wires

        bits_b = self.input  # Bob's inputs

        # Create dict mapping each wire of Bob to Bob's input
        b_inputs_clear = {
            b_wires[i]: bits_b[i]
            for i in range(len(b_wires))
        }

        logging.debug("Received Alice's inputs")
        return b_inputs_clear.items()

    def evaluate(self, a_inputs, b_inputs_encr):
        result = yao.evaluate(self.circuit, self.garbled_tables, self.pbits_out, a_inputs, b_inputs_encr)
        logging.debug("Sending circuit evaluation")
        return result


def main():
    circuits = "../circuits/and.json"

    a_input = [0, 1]
    b_input = [1, 1]

    alice = Alice(a_input, circuits)
    bob = Bob(b_input)

    # Round 1: Alice
    alice.garble_circuits() # Garbles circuits, alice stores them
    circuit = alice.garbled_circuits[0] # and.json contains only a single circuit
    a_inputs = alice.send_inputs() # Sends alice's inputs

    # Round 2: Bob
    b_inputs = bob.receive_circuits_and_inputs(circuit, a_inputs) # Bob receives inputs and keys and prepares for OT
    b_inputs_encr = {}

    # Perform OT over the inputs
    for w, b in b_inputs:
        G,c = alice.ot_send()
        h0 = bob.ot_send(b,G,c)
        c1, e0, e1 = alice.ot_receive(w, h0)
        b_inputs_encr[w] = pickle.loads(bob.ot_receive(b, c1, e0, e1))

    res = bob.evaluate(a_inputs, b_inputs_encr)
    print("Circuit Output", res) # Final outputs

main()